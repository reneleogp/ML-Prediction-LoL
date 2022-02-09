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
                "Blue Mastery 1",
                "Blue Mastery 2",
                "Blue Mastery 3",
                "Blue Mastery 4",
                "Blue Mastery 5",
                "Blue Masteries Avg",
                "Blue Masteries Median",
                "Blue Masteries Kurtorsis",
                "Blue Masteries Skewness",
                "Blue Masteries Std",
                "Blue Masteries Variance",
                # Blue Winrates Data
                "Blue Winrate 1",
                "Blue Winrate 2",
                "Blue Winrate 3",
                "Blue Winrate 4",
                "Blue Winrate 5",
                "Blue Winrates Avg",
                "Blue Winrates Median",
                "Blue Winrates Kurtorsis",
                "Blue Winrates Skewness",
                "Blue Winrates Std",
                "Blue Winrates Variance",
                # Red Masteries Data
                "Red Mastery 1",
                "Red Mastery 2",
                "Red Mastery 3",
                "Red Mastery 4",
                "Red Mastery 5",
                "Red Masteries Avg",
                "Red Masteries Median",
                "Red Masteries Kurtorsis",
                "Red Masteries Skewness",
                "Red Masteries Std",
                "Red Masteries Variance",
                # Red Winrates Data
                "Red Winrate 1",
                "Red Winrate 2",
                "Red Winrate 3",
                "Red Winrate 4",
                "Red Winrate 5",
                "Red Winrates Avg",
                "Red Winrates Median",
                "Red Winrates Kurtorsis",
                "Red Winrates Skewness",
                "Red Winrates Std",
                "Red Winrates Variance",
                # Final Result
                "Blue Won",
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
