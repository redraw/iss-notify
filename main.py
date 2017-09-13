import settings

from huey import RedisHuey
from redis import StrictRedis

huey = RedisHuey('iss', **settings.REDIS)
redis = StrictRedis(**settings.REDIS)