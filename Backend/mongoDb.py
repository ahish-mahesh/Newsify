import pymongo
import requests
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

newsifyDb = myclient["newsify"]

# dblist = myclient.list_database_names()
# if "mydatabase" in dblist:
#     print("The database exists.")

users = newsifyDb["users"]

for x in users.find({}, {"_id": 0}):
    print(json.dumps(x, indent=1))

# mydict = {
#     "username": "ahish",
#     "password": "1234",
# }

# x = users.insert_one(mydict)

# print(len(list(users.find({"username": "ahish"}))))

# result = users.delete_many({})


# print(result.deleted_count, " documents deleted.") 

# sources = newsifyDb["sources"]

# response = requests.get("https://newsapi.org/v2/sources?language=en&apiKey=7ac4dc02591646bf91c5a3ccf45633f4")

# x = sources.insert_many(response.json()["sources"])

# result = sources.find({}, {"_id": 0, "id": 1, "name": 1})

# for x in result:
#     print(x)

# print(json.dumps(response.json()["sources"], indent = 1))