# -*- coding: utf-8 -*-
import json
import logging
import time
from pytz import utc
from datetime import datetime, timedelta
from huey import crontab

import settings
from main import huey, redis
from services import OneSignal
from heavens import HeavensAbove

logger = logging.getLogger(__name__)


@huey.task(include_task=True)
def alert(location, data, task=None):
    redis.srem('iss:schedule:%s' % location, task.task_id)

    if datetime.utcnow() < data['end']['datetime']:
        logger.info("ISS above on %s!" % location)
        OneSignal().send_pass_notification(location, data)


interval = crontab(minute=settings.CHECK_INTERVAL_MINUTES)
@huey.periodic_task(interval)
def schedule():
    """Schedule passes for all locations that hasn't pending passes"""
    #push_service = OneSignal()

    for location in redis.smembers('iss:locations'):

        schedule = 'iss:schedule:%s' % location

        if redis.exists(schedule):
            continue

        lat, lng = location.split(',')

        ha = HeavensAbove(lat, lng)

        for next_pass in ha.get_next_passes():
            logger.info("Scheduling ISS pass for %s" % location)

            # >> Schedule pass in OneSignal
            # push_service.send_pass_notification(location, next_pass, schedule=True)

            # >> Schedule pass in Redis
            eta = next_pass['start']['datetime'].replace(tzinfo=utc)
            q = alert.schedule(args=[location, next_pass], eta=eta)
            redis.sadd(schedule, q.task.task_id)

        # Limit requests
        time.sleep(2)
