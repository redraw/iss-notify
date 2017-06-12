# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime, timedelta
from huey import crontab

import iss
from config import huey, hooks

logger = logging.getLogger(__name__)


@huey.task()
def alert(data):
    logger.info("ISS pass!")
    hooks.trigger('on_pass', data['duration'])


@huey.periodic_task(crontab(minute='*/10'))
def check_next_pass():

    if huey.scheduled():
        return

    next_passes = iss.get_next_pass('-34.9058', '-57.9560')
    #next_passes = iss.mock()
    
    if not next_passes:
        return

    for next_pass in next_passes:
        risetime = next_pass['risetime']
        eta = datetime.fromtimestamp(risetime)
        alert.schedule(args=[next_pass], eta=eta)
