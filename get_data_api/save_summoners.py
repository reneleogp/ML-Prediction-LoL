import json
from pymongo import MongoClient
import time
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client.league

batch = 0
db = client.league
collection = db['na_summoners']

with open('NA_summoners.json') as json_file:
    data = json.load(json_file)

cnt = 0
totalBatches = len(data)
for summoner in data:
    batch += 1
    collection.update_one({'summonerName': summoner['summonerName']},
                          {"$set": summoner}, upsert=True)
    cnt += 1
    print(f"Processing file {batch} ({100*batch//totalBatches}%)")

end = time.time()
print(f'Time taken: {end - start}')
