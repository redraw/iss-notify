import re
from datetime import datetime, timedelta

import requests
from collections import namedtuple
from bs4 import BeautifulSoup
from urlparse import parse_qs

from utils import julian


class SatID:
    ISS = 25544


class HeavensAbove:
    """UNOFFICIAL
    Hey! this data should be available somewhere in the world?
    """

    BASE_URL = "http://heavens-above.com"
    URL_PASSES = "{}/PassSummary.aspx".format(BASE_URL)

    PassRow = namedtuple('PassRow', [
        'date',
        'mag',
        'start_time',
        'start_alt',
        'start_az',
        'highest_time',
        'highest_alt',
        'highest_az',
        'end_time',
        'end_alt',
        'end_az',
        'pass_type'
    ])

    def __init__(self, lat, lng):
        self.session = requests.Session()
        self.lat = lat
        self.lng = lng

    def get_next_passes(self, *args, **kwargs):
        passes = self.get_passes(*args, **kwargs)
        now = datetime.utcnow()

        return filter(lambda p: p['start']['datetime'] > now, passes)

    def get_passes(self, satid=SatID.ISS):
        response = self.session.get(HeavensAbove.URL_PASSES, params={
            'satid': satid,
            'lat': self.lat,
            'lng': self.lng
        })

        passes = self._parse_passes(response.text)

        return passes

    def _parse_passes(self, html):
        passes = []

        dom = BeautifulSoup(html, 'html.parser')

        for tr in dom.select('tr.clickableRow'):
            p = HeavensAbove.PassRow(*[unicode(td.string) for td in tr.children])

            link = self._get_pass_link(tr)
            year = self._get_pass_year(link)

            passes.append({
                'url': '{}/{}'.format(HeavensAbove.BASE_URL, link),
                'mag': p.mag,
                'start': {
                    'datetime': datetime.strptime("%s %s %s" % (p.date, p.start_time, year), "%d %b %X %Y"),
                    'alt': p.start_alt,
                    'az': p.start_az
                },
                'highest': {
                    'datetime': datetime.strptime("%s %s %s" % (p.date, p.highest_time, year), "%d %b %X %Y"),
                    'alt': p.highest_alt,
                    'az': p.highest_az
                },
                'end': {
                    'datetime': datetime.strptime("%s %s %s" % (p.date, p.end_time, year), "%d %b %X %Y"),
                    'alt': p.end_alt,
                    'az': p.end_az
                }
            })

        return passes

    def _get_pass_link(self, tr):
        return re.match(r"window.location='(.*)'", tr.attrs['onclick']).group(1)

    def _get_pass_year(self, link):
        """No full date in table
        Getting year from Modified Julian Date inside detail's link parameter
        """
        mjd = float(parse_qs(link)['mjd'][0])
        jd = julian.mjd_to_jd(mjd)
        dt = julian.jd_to_datetime(jd)

        return dt.year
