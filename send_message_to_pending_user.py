from pprint import pprint
from typing import Mapping, Any

import pymongo
from bale import Bot
from pymongo.collection import Collection

from setting import BALE_TOKEN

client = Bot(token=BALE_TOKEN)

pending_user_message_text = '''سلام بر شما دوست عزیز !
ثبت نام شما هنوز تکمیل نشده است.
با توجه به این که در آخرین روز های ثبت نام قرار داریم. لطفا ثبت نام خود را کامل کنید.
برای این کار میتوانید روی دکمه زیر کلیک کنید'''
start_message = '/start'

edit_iq_message = '''سلامی دوباره!
در صورتی که میخواید پاسخ سوالات تست هوش رو تغییر بدید از دکمه زیر استفاده کنید.
فقط کاملا دقت کنید که با زدن گزینه زیر تمام پاسخ های قبلی شما حذف خواهد شد.'''
edit_iq_btn = "/edit_iq_test"

@client.event
async def on_ready():
    await send_message_to_user(db)


async def send_message_to_user(data_base: Collection[Mapping[str, Any]], pending_user=False):
    for student in data_base.find():
        print(student['_id'])
        if (('finished' in student and not student[
            'finished']) or 'IQ-q2' not in student or 'finished' not in student) or not pending_user:
            user = await client.get_user(student['_id'])
            if user:
                await user.send(edit_iq_message)
                await user.send(edit_iq_btn)


if __name__ == "__main__":
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = my_client["baleBotDB"]
    db = mydb["students"]
    client.run()
