import json
import ephem
import logging
import requests

from datetime import datetime
from math import degrees
from utils import az_to_octant
from collections import namedtuple

logger = logging.getLogger(__name__)


# testing
tle = """ISS (ZARYA)
1 25544U 98067A   17188.54872024  .00016717  00000-0  10270-3 0  9026
2 25544  51.6424 296.8358 0005125   5.6292 354.4917 15.54172114 24912""".split('\n')


EphemPass = namedtuple('EphemPass', [
    'rise_time',
    'rise_az',
    'max_alt_time',
    'max_alt',
    'set_time',
    'set_az'
])


class SatID:
    ISS = 25544


class SatTracker(object):

    def __init__(self, lat, lon, horizon='10', satid=SatID.ISS):
        #tle = HA.get_tle(satid)

        self.observer = ephem.Observer()
        self.observer.lat = lat
        self.observer.lon = lon

        # disable atmospheric reflection
        self.observer.pressure = 0
        self.observer.horizon = horizon

        self.sun = ephem.Sun()

        self.satellite = ephem.readtle(*tle)

    def get_next_passes(self, n=15, visible_only=False):
        passes = []

        self.observer.date = datetime.utcnow()

        computed_pass = self.yield_next_pass()

        for _ in range(n):
            p = next(computed_pass)
            passes.append(p)

        if visible_only:
            return filter(lambda p: p['visible'], passes)

        return passes

    def yield_next_pass(self):
        """Yield next pass for observer/satellite"""

        while True:
            try:
                next_pass = self.observer.next_pass(self.satellite)
            except ephem.CircumpolarError:
                # no passes for you!
                logger.info(
                    "Tried to calculate passes for circumpolar sat"
                    "@ {}".format(self.observer)
                )
                raise

            _pass = EphemPass(*next_pass)

            yield self.compute_pass(_pass)

            # advance 5 minutes after pass
            self.observer.date = _pass.set_time + (5 * ephem.minute)

    def compute_pass(self, _pass):
        """_pass is an EphemPass
        Computes visibility and formatting of the pass"""

        visible = False
        passing_time = _pass.rise_time

        while passing_time < _pass.set_time:
            passing_time += ephem.second
            self.observer.date = passing_time

            self.sun.compute(self.observer)
            self.satellite.compute(self.observer)

            if (
                not self.satellite.eclipsed and
                -18 < degrees(self.sun.alt) < -6
            ):
                visible = True
                break

        # set highest azimuth
        self.observer.date = _pass.max_alt_time
        self.satellite.compute(self.observer)
        highest_az = self.satellite.az

        # todo: missing visible start/end/highest values

        return {
            'start': {
                'datetime': _pass.rise_time.datetime(),
                'alt': degrees(self.observer.horizon),
                'az': az_to_octant(_pass.rise_az)
            },
            'highest': {
                'datetime': _pass.max_alt_time.datetime(),
                'alt': degrees(_pass.max_alt),
                'az': az_to_octant(highest_az)
            },
            'end': {
                'datetime': _pass.set_time.datetime(),
                'alt': degrees(self.observer.horizon),
                'az': az_to_octant(_pass.set_az)
            },
            'visible': visible
        }


class TLE(object):

    FEED_URL = "http://www.celestrak.com/NORAD/elements/stations.txt"

    def __init__(self):
        self.session = requests.Session()

    def update(self):
        r = self.session.get(TLE.FEED_URL)
        lines = [line.strip() for line in r.text.split('\n') if line]

        satellites = []

        for i in range(0, len(lines), 3):
            satellites.append(lines[i:i+3])

        with open('tle.json', 'w') as f:
            json.dump(satellites, f, indent=4)
