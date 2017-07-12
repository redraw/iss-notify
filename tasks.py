# -*- coding: utf-8 -*-
import json
import logging
from pytz import utc
from datetime import datetime, timedelta
from huey import crontab

import settings
from main import huey, hooks
from heavens import HeavensAbove
from tle import SatTracker, TLE

logger = logging.getLogger(__name__)


@huey.task()
def alert(data):
    if datetime.utcnow() < data['end']['datetime']:
        logger.info("ISS above!")
        hooks.trigger('on_pass', data)
    else:
        logger.info("Missed ISS alert at %s" % data['start']['datetime'])


interval = crontab(minute=settings.CHECK_INTERVAL_MINUTES)
@huey.periodic_task(interval)
def check():
    if huey.scheduled():
       logger.info("ISS passes already scheduled")
       return

    if settings.USE_HEAVENS_ABOVE:
        calculator = HeavensAbove(settings.LAT, settings.LNG)
    else:
        calculator = SatTracker(settings.LAT, settings.LNG)

    for next_pass in calculator.get_next_passes(visible_only=True):
        eta = next_pass['start']['datetime'].replace(tzinfo=utc)
        alert.schedule(args=[next_pass], eta=eta)


interval = crontab(hour=settings.TLE_UPDATE_INTERVAL_HOURS)
@huey.periodic_task(interval)
def update_tle():
    logger.info("Updating TLE...")
    TLE().update()


# update at startup
#update_tle()