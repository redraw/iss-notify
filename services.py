import os
import json
import datetime
import requests
import logging
import settings

from main import redis

logger = logging.getLogger(__name__)


class OneSignal(object):

    NOTIFICATIONS_URL = "https://onesignal.com/api/v1/notifications"
    PLAYERS_URL = "https://onesignal.com/api/v1/players"

    def __init__(self, api_key=settings.ONESIGNAL_API_KEY):
        self.session = requests.Session()

        self.session.headers.update({
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": "Basic {}".format(api_key)
        })

    def send_notification(self, *args, **kwargs):
        payload = {"app_id": settings.ONESIGNAL_APP_ID}
        payload.update(kwargs)

        response = self.session.post(OneSignal.NOTIFICATIONS_URL, data=json.dumps(payload))
        data = response.json()

        if data.get('errors'):
            invalid_player_ids = data['errors'].get('invalid_player_ids', [])
            for player_id in invalid_player_ids:
                redis.srem('iss:location:%s:players' % location, player_id)

        return response

    def send_pass_notification(self, location, data, schedule=False):
        start_dt = data['start']['datetime']
        end_dt = data['end']['datetime']
        duration = end_dt - start_dt
        ttl = duration.seconds

        payload = {
            "filters": [
                {"field": "tag", "key": "location", "relation": "=", "value": location}
            ],
            "headings": {"en": "ISS above"},
            "contents": {
                "en": u"Magnitude: {mag}. Highest point: {alt} {az}".format(
                    mag=data['mag'],
                    alt=data['highest']['alt'],
                    az=data['highest']['az'],
                )
            },
            "url": data['url'],
            "ttl": ttl
        }

        if schedule:
            payload.update({'send_after': start_dt.isoformat() })

        response = self.send_notification(**payload)
        data = response.json()

        logger.info("Notification sent: %s (recipients: %s)" % (location, data['recipients']))

    def get_device(self, player_id):
        params = {"app_id": settings.ONESIGNAL_APP_ID}

        url = "{}/{}".format(OneSignal.PLAYERS_URL, player_id)
        response = self.session.get(url, params=params)

        device = {}

        if response.ok:
            device = response.json()

        return device
