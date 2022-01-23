import requests
import json
from pymongo import MongoClient
import time
from bs4 import BeautifulSoup

client = MongoClient("mongodb://admin:P4ssw0rd@107.190.2.229:27018")

db = client.league
start = time.time()


def save_champion_mastery(summonerName, region):
    collection = db['masteries']
    url = "https://championmastery.gg/summoner?summoner=PlayErphil&region=LAN"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find("tbody", id="tbody")

    job_elements = results.find_all("tr")

    for job_element in job_elements:
        print(job_element.text.replace(" ", ""), end="\n"*2)

    # for game in games_list:
    #     collection.update_one({'matchId': game['matchId']},
    #                           {"$setOnInsert": game}, upsert=True)


save_champion_mastery("pentaculos3k", "LAN")
# save_champion_mastery("andyspr666", "LAN")


end = time.time()

print(f"Time taken: {end - start} s")
