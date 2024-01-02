
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["baleBotDB"]
db = mydb["students"]

q = db.find()
for i in q:
    print(i)