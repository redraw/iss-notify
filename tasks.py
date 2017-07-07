# -*- coding: utf-8 -*-
import json
import logging
import requests
from datetime import datetime, timedelta
from huey import crontab

import iss
import settings

from main import huey, hooks, redis

logger = logging.getLogger(__name__)


@huey.task()
def alert(data):
    risetime = datetime.fromtimestamp(data['risetime'])
    threshold = timedelta(seconds=data['duration'])

    if datetime.now() < risetime + threshold:
        logger.info("ISS above!")
        hooks.trigger('on_pass', data['duration'])
    else:
        logger.info("Missed ISS alert at %s" % risetime)


interval = crontab(minute=settings.CHECK_INTERVAL_MINUTES)
@huey.periodic_task(interval)
def check():
    if huey.scheduled():
        return

    next_passes = iss.get_next_passes(
        settings.LAT, settings.LNG,
        visible_only=settings.VISIBLE_ONLY
    )

    for next_pass in next_passes:
        risetime = next_pass['risetime']
        eta = datetime.fromtimestamp(risetime)
        alert.schedule(args=[next_pass], eta=eta)


interval = crontab(hour=settings.TLE_INTERVAL_HOURS)
@huey.periodic_task(interval)
def update_tle():
    logger.info("Updating TLE")

    r = requests.get('http://www.celestrak.com/NORAD/elements/stations.txt')
    lines = [line for line in r.text.split('\n') if line]

    stations = []

    for i in range(0, len(lines), 3):
        stations.append(lines[i:i+3])

    iss = stations[0]
    redis.set('iss:tle', json.dumps(iss))


# update at startup
update_tle()
