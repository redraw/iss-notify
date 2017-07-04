import json
import ephem
import datetime
from collections import namedtuple

from main import redis


EphemPass = namedtuple('EphemPass', [
    'rise_time',
    'rise_az',
    'max_alt_time',
    'max_alt',
    'set_time',
    'set_az']
)


def get_next_passes(lat, lng, elevation=30, n=5):

    tle = redis.get('iss:tle')

    if not tle:
        return

    tle0, tle1, tle2 = json.loads(tle)

    iss = ephem.readtle(str(tle0), str(tle1), str(tle2))

    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lng
    observer.elevation = elevation

    observer.pressure = 0
    observer.horizon = '10'

    passes = []

    for i in range(n):
        p = EphemPass(*observer.next_pass(iss))

        passes.append({
            'risetime': p.rise_time,
            'duration': datetime.timedelta(p.set_time - p.rise_time).seconds
        })

        observer.date = p.set_time + (5 * ephem.minute)
