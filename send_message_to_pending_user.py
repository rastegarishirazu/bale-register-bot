import asyncio
from pprint import pprint
from typing import Mapping, Any

import pymongo
from bale import Bot
from pymongo.collection import Collection

from setting import BALE_TOKEN

client = Bot(token=BALE_TOKEN)

message_text = '''سلام بر شما دوست عزیز !
ثبت نام شما هنوز تکمیل نشده است.
با توجه به این که در آخرین روز های ثبت نام قرار داریم. لطفا ثبت نام خود را کامل کنید.
برای این کار میتوانید روی دکمه زیر کلیک کنید'''
start_message = '/start'


@client.event
async def on_ready():
    await send_message_to_pending_user(db)


async def send_message_to_pending_user(db: Collection[Mapping[str, Any]]):
    for user in db.find():
        print(user['_id'])
        if ('finished' in user and not user['finished']) or 'IQ-q2' not in user or 'finished' not in user:
            user = await client.get_user(user['_id'])
            if user:
                await user.send(message_text)
                await user.send(start_message)


if __name__ == "__main__":
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = my_client["baleBotDB"]
    db = mydb["students"]
    client.run()
