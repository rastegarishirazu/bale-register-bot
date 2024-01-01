import pymongo
from content import RegisterMode

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["baleBotDB"]
db = mydb["students"]
db.drop()
# db.insert_one({"_id": "1234"})
# db.update_one({"_id": "1234"}, {"$set": {RegisterMode.FIRST_NAME.value: "ali"}})
# std = db.find_one({"_id": "1234"})
# print(std)
