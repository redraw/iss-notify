from huey import RedisHuey
from hooks import HookManager
from dotenv import load_dotenv, find_dotenv


huey = RedisHuey('iss')
hooks = HookManager()

# load .env
load_dotenv(find_dotenv())
