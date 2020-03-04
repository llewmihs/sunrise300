from asyncpushbullet import AsyncPushbullet
from config import *

pb = AsyncPushbullet(PUSHBULLET)

push = await pb.async_push_note("Title","Body")