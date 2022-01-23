import requests
import json

url = "https://app.mobalytics.gg/api/lol/graphql/v1/query"

payload = json.dumps({
    "operationName": "LolProfilePageQuery",
    "variables": {
        "withMatchParticipantDetailed": False,
        "region": "LAN",
        "summonerName": "pentaculos3k",
        "sQueue": None,
        "sRole": None,
        "sChampion": None,
        "cQueue": "RANKED_SOLO",
        "cRolename": None,
        "cChampionId": None,
        "cLpPerPage": 150,
        "cLpPageIndex": 1,
        "cSortField": "GAMES",
        "cSortDirection": "DESC",
        "withSummonerBase": True,
        "withSummonerQueue": False,
        "withSummonerPerformance": False,
        "withOverviewSection": False,
        "withChampionsPoolSection": True,
        "withMatchupsPoolSection": False,
        "withLpGainSection": False
    },
    "extensions": {
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "5140d5473804b12a9c273896ca1f59f23461d89a6d9fa9b956cd4160ee5f8974"
        }
    }
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)


python_file = open("response.json", "w")

python_file.write(response.text)
python_file.close()
