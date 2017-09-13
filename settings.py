import os

CHECK_INTERVAL_MINUTES = os.getenv('CHECK_INTERVAL_MINUTES', '*/60')
ONESIGNAL_APP_ID = os.getenv('ONESIGNAL_APP_ID', '')
ONESIGNAL_API_KEY = os.getenv('ONESIGNAL_API_KEY', '')

REDIS = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': os.getenv('REDIS_PORT', '6379'),
    'password': os.getenv('REDIS_PASS', '')
}

MAP_FILE = 'map.html'
