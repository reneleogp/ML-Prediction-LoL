import csv
from pymongo import MongoClient
import statistics_functions as stats
import time
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client.league
t0 = time.time()


def add_data(raw_data) -> list:
    processed_data = []

    # add 5
    processed_data += raw_data
    # add 6
    processed_data.append(stats.average(raw_data))
    processed_data.append(stats.median(raw_data))
    processed_data.append(stats.kurtosis(raw_data))
    processed_data.append(stats.skewness(raw_data))
    processed_data.append(stats.standard_deviation(raw_data))
    processed_data.append(stats.variance(raw_data))

    # return 11
    return processed_data


with open('new1_set.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    batch = 0

    totalBatches = db.matches.count_documents({})
    cursor = db.matches.find({}, no_cursor_timeout=True,  batch_size=1)
    for match in cursor:
        t1 = time.time()
        batch += 1
        print(f"Processing file {batch} ({100*batch//totalBatches}%)", end="")
        # check if the match is valid
        if(match['masteries'] == False or match['winrates'] == False or match['processed'] == True):
            continue

        blueWinrates = []
        blueMasteries = []
        redWinrates = []
        redMasteries = []
        participants = match['participants']
        region = match['subject']['region']

        for participant in participants:
            summonerName = participant['summonerName']
            championId = participant['championId']
            team = participant['team']

            try:
                mastery_list = db.masteries.find_one(
                    {'summonerName': summonerName})['mastery']
            except:
                print(summonerName)
            winrate_list = db.winrates.find_one(
                {'summonerName': summonerName})['winrate']

            mastery = 0
            # Go over each element of the list
            for mastery_object in mastery_list:
                if(championId == mastery_object['championId']):
                    mastery = mastery_object['mastery']

            winrate = 0
            for winrate_object in winrate_list:
                if(championId == winrate_object['championID']):
                    winrate = winrate_object['winrate']/100

            if(team == 'RED'):
                redMasteries.append(mastery)
                redWinrates.append(winrate)
            else:
                blueMasteries.append(mastery)
                blueWinrates.append(winrate)

        blueData = []
        redData = []

        blueData += add_data(blueMasteries)
        blueData += add_data(blueWinrates)
        redData += add_data(redMasteries)
        redData += add_data(redWinrates)

        final_data = []
        final_data += blueData
        final_data += redData

        teams = {match['teams'][0]['id']: match['teams'][0]['result'],
                 match['teams'][1]['id']: match['teams'][1]['result']}

        if(teams['BLUE'] == 'WON'):
            final_data.append(1)
        else:
            final_data.append(0)

        # write the data
        writer.writerow(final_data)
        db.matches.update_one({'matchId': match['matchId']},
                              {"$set": {'processed': True}})

        t2 = time.time()
        print(" {:.2f}s (total: {:.2f}s)".format(t2-t1, t2-t0))
    cursor.close()
