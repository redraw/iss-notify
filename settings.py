import os

LAT = os.getenv('LAT', '-34.905')
LNG = os.getenv('LNG', '-57.956')
CHECK_INTERVAL_MINUTES = os.getenv('CHECK_INTERVAL_MINUTES', '*/60')
TLE_UPDATE_INTERVAL_HOURS = os.getenv('TLE_UPDATE_INTERVAL_HOURS', '*/24')
USE_HEAVENS_ABOVE = False