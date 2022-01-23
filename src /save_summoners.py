import json
from pymongo import MongoClient
import time

start = time.time()

client = MongoClient("mongodb://admin:P4ssw0rd@107.190.2.229:27018")

db = client.league
collection = db['summoners']

with open('summoners.json') as json_file:
    data = json.load(json_file)

cnt = 0
for summoner in data:
    collection.update_one({'summonerName': summoner['summonerName']},
                          {"$set": summoner}, upsert=True)
    cnt += 1
    print(cnt)

end = time.time()
print(f'Time taken: {end - start}')
