import redis
from huey import RedisHuey
from hooks import HookManager

huey = RedisHuey('iss')
hooks = HookManager()
redis = redis.StrictRedis()