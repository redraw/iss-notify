import json
import ephem
import datetime
from math import degrees
from collections import namedtuple

from main import redis


EphemPass = namedtuple('EphemPass', [
    'rise_time',
    'rise_az',
    'max_alt_time',
    'max_alt',
    'set_time',
    'set_az'
])


def get_next_passes(lat, lng, elevation=30, n=15, visible_only=False):

    tle = redis.get('iss:tle').decode()

    if not tle:
        return []

    tle0, tle1, tle2 = json.loads(tle)

    sat = ephem.readtle(str(tle0), str(tle1), str(tle2))

    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lng
    observer.elevation = elevation

    observer.pressure = 0
    observer.horizon = '10'

    sun = ephem.Sun()

    passes = []

    for i in range(n):
        next_pass = observer.next_pass(sat)
        p = EphemPass(*next_pass)

        t = p.rise_time
        visible = False

        while t < p.set_time:
            t += ephem.second
            observer.date = t

            sat.compute(observer)
            sun.compute(observer)

            if not sat.eclipsed and -18 < degrees(sun.alt) < -6:
                visible = True
                break

        passes.append({
            'risetime': p.rise_time,
            'duration': datetime.timedelta(p.set_time - p.rise_time).seconds,
            'visible': visible
        })

        observer.date = p.set_time + (5 * ephem.minute)

    if visible_only:
        return filter(lambda p: p['visible'], passes)

    return passes
