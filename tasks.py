# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime, timedelta
from huey import crontab

import iss
import settings

from main import huey, hooks

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


@huey.periodic_task(crontab(minute=settings.CHECK_INTERVAL_MINUTES))
def check():

    if huey.scheduled():
        logger.info("No ISS passes scheduled.")
        return

    next_passes = iss.get_next_passes(settings.LAT, settings.LNG)
    #next_passes = iss.mock()
    
    if not next_passes:
        return

    for next_pass in next_passes:
        risetime = next_pass['risetime']
        eta = datetime.fromtimestamp(risetime)
        alert.schedule(args=[next_pass], eta=eta)
