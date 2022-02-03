import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client.league


db = client.league
collection = db["na_summoners"]

with open("NA_summoners.json") as json_file:
    data = json.load(json_file)

batch = 0
totalBatches = len(data)
for summoner in data:
    batch += 1
    print(f"Processing file {batch} ({100*batch//totalBatches}%)")
    collection.update_one(
        {"summonerName": summoner["summonerName"]}, {"$set": summoner}, upsert=True
    )
