import pymongo
import sys
from content import RegisterMode

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["baleBotDB"]
db = mydb["students"]

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'RESET-DB':
        db.drop()
        print('data base cleaned!')
    else:
        print('use RESET-DB')
