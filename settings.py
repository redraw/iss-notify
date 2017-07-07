import os

LAT = os.getenv('LAT', '-34.905')
LNG = os.getenv('LNG', '-57.956')
CHECK_INTERVAL_MINUTES = os.getenv('CHECK_INTERVAL_MINUTES', '*/10')
TLE_INTERVAL_HOURS = os.getenv('TLE_INTERVAL_HOURS', '*/24')
VISIBLE_ONLY = True
