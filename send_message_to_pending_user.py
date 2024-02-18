from pprint import pprint
from typing import Mapping, Any

import pymongo
from bale import Bot
from pymongo.collection import Collection

from setting import BALE_TOKEN

client = Bot(token=BALE_TOKEN)


def send_message_to_pending_user(db: Collection[Mapping[str, Any]]):
    for user in db.find():
        pprint(user)


if __name__ == "__main__":
    my_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = my_client["baleBotDB"]
    db = mydb["students"]
    send_message_to_pending_user(db)
