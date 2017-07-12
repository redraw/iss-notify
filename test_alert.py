# -*- coding: utf-8 -*-
import sys
import datetime
import settings
from tasks import alert

from main import redis


def test(location):

    iss_pass = {
        'mag': '-3.5',
        'start': {
            'datetime': datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        },
        'highest': {
            'alt': u"39°",
            'az': u"NNE",
            'datetime': datetime.datetime.utcnow() + datetime.timedelta(seconds=15)
        },
        'end': {
            'datetime': datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        },
        'url': 'http://heavens-above.com'
    }

    t = alert.schedule(args=[location, iss_pass])
    r.sadd('iss:schedule:%s' % location, t.task.task_id)


if __name__ == '__main__':

    location = '-35,-58' # La Plata

    if len(sys.argv) > 1:
        location = sys.argv[1]

    test(location)