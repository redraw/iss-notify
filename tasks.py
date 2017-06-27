# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime, timedelta
from huey import crontab

import settings
from heavens import HeavensAbove

from main import huey, hooks

logger = logging.getLogger(__name__)


@huey.task()
def alert(data):
    if datetime.now() < data['end']['datetime']:
        logger.info("ISS above!")
        hooks.trigger('on_pass', data)
    else:
        logger.info("Missed ISS alert at %s" % risetime)


@huey.periodic_task(crontab(minute=settings.CHECK_INTERVAL_MINUTES))
def check():
    if huey.scheduled():
        logger.info("ISS passes already scheduled")
        return

    lat, lng = settings.LAT, settings.LNG

    next_passes = HeavensAbove(lat, lng).get_next_passes()

    for next_pass in next_passes:
        eta = next_pass['start']['datetime']
        alert.schedule(args=[next_pass], eta=eta)
