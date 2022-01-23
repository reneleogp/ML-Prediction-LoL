import requests
import json

url = "https://u.gg/api"

payload = json.dumps({
    "operationName": "getPlayerStats",
    "variables": {
        "summonerName": "pentaculos3k",
        "regionId": "la1",
        "role": 7,
        "seasonId": 17,
        "queueType": [
            420
        ]
    },
    "query": "query getPlayerStats($queueType: [Int!], $regionId: String!, $role: Int!, $seasonId: Int!, $summonerName: String!) {\n  fetchPlayerStatistics(\n    queueType: $queueType\n    summonerName: $summonerName\n    regionId: $regionId\n    role: $role\n    seasonId: $seasonId\n  ) {\n    basicChampionPerformances {\n      championId\n      totalMatches\n      wins\n      __typename\n    }\n    exodiaUuid\n    puuid\n    queueType\n    regionId\n    role\n    seasonId\n    __typename\n  }\n}\n"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
