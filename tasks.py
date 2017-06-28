# -*- coding: utf-8 -*-
import json
import logging
from pytz import utc
from datetime import datetime, timedelta
from huey import crontab

import settings
from main import huey, hooks
from heavens import HeavensAbove

logger = logging.getLogger(__name__)


@huey.task()
def alert(data):
    if datetime.utcnow() < data['end']['datetime']:
        logger.info("ISS above!")
        hooks.trigger('on_pass', data)
    else:
        logger.info("Missed ISS alert at %s" % data['start']['datetime'])


@huey.periodic_task(crontab(minute=settings.CHECK_INTERVAL_MINUTES))
def check():
    if huey.scheduled():
       logger.info("ISS passes already scheduled")
       return

    ha = HeavensAbove(settings.LAT, settings.LNG)

    for next_pass in ha.get_next_passes():
        eta = next_pass['start']['datetime'].replace(tzinfo=utc)
        alert.schedule(args=[next_pass], eta=eta)
