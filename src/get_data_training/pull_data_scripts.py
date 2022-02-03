from riotwatcher import LolWatcher
from pymongo import MongoClient
from api_calls import get_winrates, get_past_matches, get_masteries
from json import dumps
import time
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client.league

# Save summoners into a file


def get_randoms_summoners(region: str) -> None:
    RIOT_API_KEY = os.getenv("RIOT_API_KEY")
    lol_watcher = LolWatcher(RIOT_API_KEY)
    tier_list = ["IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]
    rank_list = ["I", "II", "III", "IV"]

    players = list()
    for tier in tier_list:
        for division in rank_list:
            players.extend(
                lol_watcher.league.entries(region, "RANKED_SOLO_5x5", tier, division)
            )

    with open(f"{region}_summoners.json", "w") as file:
        file.write(dumps(players))

    size = len(players)
    print(size)


# Get Matches


def get_all_matches():
    t0 = time.time()
    batch = 0
    to_collection = db["na_matches"]
    from_collection = db["na_summoners"]
    top = 1  # Number of most recent last matches you want per summoner
    totalBatches = from_collection.count_documents({})

    cursor = from_collection.find({}, no_cursor_timeout=True, batch_size=1)
    for summoner in cursor:
        t1 = time.time()
        batch += 1
        print(f"Processing file {batch} ({100*batch//totalBatches}%)", end="")
        summonerName = summoner["summonerName"]
        region = "NA"

        matches_list = get_past_matches(summonerName, region, top)

        if matches_list == None:
            continue

        for match in matches_list:
            if to_collection.find_one({"matchId": match["matchId"]}):
                print("Skipped match!")
                continue
            match["processed"] = False
            to_collection.update_one(
                {"matchId": match["matchId"]}, {"$setOnInsert": match}, upsert=True
            )

        t2 = time.time()
        print(" {:.2f}s (total: {:.2f}s)".format(t2 - t1, t2 - t0))
    cursor.close()


# Get Masteries


def get_all_masteries():
    t0 = time.time()
    batch = 0
    to_collection = db["masteries"]
    from_collection = db["na_matches"]
    totalBatches = from_collection.count_documents({}) * 10
    cursor = from_collection.find({}, no_cursor_timeout=True, batch_size=1)

    for match in cursor:
        participants = match["participants"]
        region = match["subject"]["region"]
        invalid_match = False

        for participant in participants:
            summonerName = participant["summonerName"]
            batch += 1

            if to_collection.find_one({"summonerName": summonerName, "region": region}):
                print(f"Masteries found! {batch} / {totalBatches}")
                continue

            mastery = get_masteries(summonerName, region)
            if mastery == None:
                invalid_match = True
                continue

            to_collection.insert_one(mastery)
            print(f"Masteries added! {batch} / {totalBatches}")

        if invalid_match:
            print("Invalid Match :(")
            from_collection.update_one(
                {"matchId": match["matchId"]}, {"$set": {"masteries": False}}
            )
        else:
            print("Valid Match!")
            from_collection.update_one(
                {"matchId": match["matchId"]}, {"$set": {"masteries": True}}
            )
    cursor.close()


# Get Winrates
def get_all_winrates():
    t0 = time.time()
    batch = 0
    to_collection = db["winrates"]
    from_collection = db["na_matches"]
    totalBatches = from_collection.count_documents({}) * 10
    cursor = from_collection.find({}, no_cursor_timeout=True, batch_size=1)

    for match in cursor:
        participants = match["participants"]
        region = match["subject"]["region"]
        invalid_match = False

        for participant in participants:
            summonerName = participant["summonerName"]
            batch += 1

            if to_collection.find_one({"summonerName": summonerName, "region": region}):
                print(f"Winrates found! {batch} / {totalBatches}")
                continue

            winrate = get_winrates(summonerName, region)
            if winrate == None:
                invalid_match = True
                continue

            to_collection.insert_one(winrate)
            print(f"Winrates added! {batch} / {totalBatches}")

        if invalid_match:
            print("Invalid Match :(")
            from_collection.update_one(
                {"matchId": match["matchId"]}, {"$set": {"winrates": False}}
            )
        else:
            print("Valid Match!")
            from_collection.update_one(
                {"matchId": match["matchId"]}, {"$set": {"winrates": True}}
            )

    cursor.close()


# get_all_matches()
# get_all_masteries()
# get_all_winrates()
# ALLWAYS CLOSE THE CURSOR
