import csv
from pymongo import MongoClient
import numpy as np
import scipy.stats
import time
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client.league
t0 = time.time()


def add_stats(raw_data) -> list:
    processed_data = []

    # add 5
    processed_data += raw_data
    # add 6
    # Add average
    processed_data.append(np.average(raw_data))
    # Add median
    processed_data.append(np.median(raw_data))
    # Add coeficient of kurtosis
    processed_data.append(scipy.stats.kurtosis(raw_data, bias=False))
    # Add coeficient skewness
    processed_data.append(scipy.stats.skew(raw_data, bias=False))
    # Add standard_deviation
    processed_data.append(np.std(raw_data))
    # Add variance
    processed_data.append(np.var(raw_data))

    # return 11
    return processed_data


def process_mongo_data():
    with open("dataset.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        header = []

        writer.writerow(
            [
                # Blue Masteries Data
                "BlueMastery1",
                "BlueMastery2",
                "BlueMastery3",
                "BlueMastery4",
                "BlueMastery5",
                "BlueMasteryAvg",
                "BlueMasteryMedian",
                "BlueMasteryKurtorsis",
                "BlueMasterySkewness",
                "BlueMasteryStd",
                "BlueMasteryVariance",
                # Blue Winrates Data
                "BlueWinrates1",
                "BlueWinrates2",
                "BlueWinrates3",
                "BlueWinrates4",
                "BlueWinrates5",
                "BlueWinratesAvg",
                "BlueWinratesMedian",
                "BlueWinratesKurtorsis",
                "BlueWinratesSkewness",
                "BlueWinratesStd",
                "BlueWinratesVariance",
                # Red Masteries Data
                "RedMastery1",
                "RedMastery2",
                "RedMastery3",
                "RedMastery4",
                "RedMastery5",
                "RedMasteryAvg",
                "RedMasteryMedian",
                "RedMasteryKurtorsis",
                "RedMasterySkewness",
                "RedMasteryStd",
                "RedMasteryVariance",
                # Red Winrates Data
                "RedWinrates1",
                "RedWinrates2",
                "RedWinrates3",
                "RedWinrates4",
                "RedWinrates5",
                "RedWinratesAvg",
                "RedWinratesMedian",
                "RedWinratesKurtorsis",
                "RedWinratesSkewness",
                "RedWinratesStd",
                "RedWinratesVariance",
                # Final Result
                "DidBlueWon",
            ]
        )
        batch = 0
        from_collection = db["na_matches"]
        totalBatches = from_collection.count_documents({})
        cursor = from_collection.find({}, no_cursor_timeout=True, batch_size=1)
        for match in cursor:
            t1 = time.time()
            batch += 1
            print(f"Processing file {batch} ({100*batch//totalBatches}%)", end="")
            # check if the match is valid
            if (
                match["masteries"] == False
                or match["winrates"] == False
                or match["processed"] == True
            ):
                continue

            blueWinrates = []
            blueMasteries = []
            redWinrates = []
            redMasteries = []
            participants = match["participants"]
            region = match["subject"]["region"]

            for participant in participants:
                summonerName = participant["summonerName"]
                championId = participant["championId"]
                team = participant["team"]

                try:
                    mastery_list = db.masteries.find_one(
                        {"summonerName": summonerName, "region": region}
                    )["mastery"]
                except:
                    print(summonerName)
                winrate_list = db.winrates.find_one(
                    {"summonerName": summonerName, "region": region}
                )["winrate"]

                mastery = 0
                # Go over each element of the list
                for mastery_object in mastery_list:
                    if championId == mastery_object["championId"]:
                        mastery = mastery_object["mastery"]

                winrate = 0
                for winrate_object in winrate_list:
                    if championId == winrate_object["championID"]:
                        winrate = winrate_object["winrate"] / 100

                if team == "RED":
                    redMasteries.append(mastery)
                    redWinrates.append(winrate)
                else:
                    blueMasteries.append(mastery)
                    blueWinrates.append(winrate)

            blueData = []
            redData = []

            blueData += add_stats(blueMasteries)
            blueData += add_stats(blueWinrates)
            redData += add_stats(redMasteries)
            redData += add_stats(redWinrates)

            final_data = []
            final_data += blueData
            final_data += redData

            teams = {
                match["teams"][0]["id"]: match["teams"][0]["result"],
                match["teams"][1]["id"]: match["teams"][1]["result"],
            }

            if teams["BLUE"] == "WON":
                final_data.append(1)
            else:
                final_data.append(0)

            # write the data
            writer.writerow(final_data)
            from_collection.update_one(
                {"matchId": match["matchId"]}, {"$set": {"processed": True}}
            )

            t2 = time.time()
            print(" {:.2f}s (total: {:.2f}s)".format(t2 - t1, t2 - t0))
        cursor.close()


process_mongo_data()
