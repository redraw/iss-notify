import settings

from huey import RedisHuey
from redis import StrictRedis

huey = RedisHuey('iss', **settings.REDIS_CONF)
redis = StrictRedis(**settings.REDIS_CONF)