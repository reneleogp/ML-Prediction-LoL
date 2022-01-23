import requests
import json
from pymongo import MongoClient


def get_past_games(summoner, region, top):
    url = "https://app.mobalytics.gg/api/lol/graphql/v1/query"
    payload = json.dumps({
        "operationName": "LolProfilePageMoreMatchesQuery",
        "variables": {
            "withMatchParticipantDetailed": False,
            "summonerName": summoner,
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
    return response


client = MongoClient("mongodb://admin:P4ssw0rd@192.168.0.15:27018")

db = client.league

with open('summoners.json') as json_file:
    data = json.load(json_file)


cnt = 0
for document in db.summoners.find():
    cnt += 1
    if(cnt == 2):
        break

    summonerName = document['summonerName']
    response = get_past_games(summonerName, "LAN", 2)

    python_file = open("past_games.json", "w")
    python_file.write(response.text)
    python_file.close()
