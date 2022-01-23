import requests
import json
from pymongo import MongoClient
import time

client = MongoClient("mongodb://admin:P4ssw0rd@107.190.2.229:27018")

db = client.league
start = time.time()


def save_past_games(summonerName, region, top):
    collection = db['matches']
    url = "https://app.mobalytics.gg/api/lol/graphql/v1/query"

    payload = json.dumps({
        "operationName": "LolProfilePageMoreMatchesQuery",
        "variables": {
            "withMatchParticipantDetailed": False,
            "summonerName": summonerName,
            "region": region,
            "top": top,
            "skip": 0,
            "queue": "RANKED_SOLO",
            "rolename": None
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "92fe7bcd15126c52548a71e98d1e16c6fd128692631c73a9b512ea62f072156c"
            }
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    games_list = response.json(
    )['data']['lol']['player']['matchesHistory']['matches']

    for game in games_list:
        collection.update_one({'matchId': game['matchId']},
                              {"$setOnInsert": game}, upsert=True)


save_past_games("pentaculos3k", "LAN", 2)
save_past_games("andyspr666", "LAN", 2)


end = time.time()

print(f"Time taken: {end - start} s")
