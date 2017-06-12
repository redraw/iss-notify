from redis import StrictRedis
from huey import RedisHuey
from hooks import HookManager

redis = StrictRedis()
huey = RedisHuey('iss')
hooks = HookManager()
