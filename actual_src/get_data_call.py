import time

from call_functions import get_winrates, get_past_matches, get_masteries
from pymongo import MongoClient

client = MongoClient("mongodb://admin:P4ssw0rd@192.168.0.15:27018")

db = client.league

start = time.time()


# Go though each summoner and get all of the games

# batch = 0
# collection = db['matches']
# totalBatches = db.summoners.count_documents({})*3

# for summoner in db.summoners.find():
#     summonerName = summoner['summonerName']
#     region = "LAN"
#     matches_list = get_past_matches(summonerName, region, 3)
#     for match in matches_list:
#         batch += 1
#         collection.update_one({'matchId': match['matchId']},
#                               {"$setOnInsert": match}, upsert=True)
#         print(f'Match {batch} / {totalBatches}')


# Go through each match and get all of the masteries

batch = 0
collection = db['masteries']
totalBatches = db.matches.count_documents({})*10

for match in db.matches.find():
    participants = match['participants']
    region = match['subject']['region']
    invalid_match = False

    if(batch < 48396):
        batch += 10
        print(f"Match skiped! Batch: {batch}")
        continue

    for participant in participants:
        summonerName = participant['summonerName']
        batch += 1

        if (collection.find_one({'summonerName': summonerName})):
            print(f'Masteries found! {batch} / {totalBatches}')
            continue

        mastery = get_masteries(summonerName, region)
        if(mastery == None):
            invalid_match = True
            continue
        collection.insert_one(mastery)
        print(f'Masteries added! {batch} / {totalBatches}')

    if(invalid_match):
        print("Invalid Match :(")
        db.matches.update_one({'matchId': match['matchId']},
                              {"$set": {'masteries': False}})
    else:
        print("Valid Match!")
        db.matches.update_one({'matchId': match['matchId']},
                              {"$set": {'masteries': True}})


# Go through each game and get all of the winrates

# batch = 0
# collection = db['winrates']
# totalSummoners = db.matches.count_documents({})*10

# for match in db.matches.find():

#     participants = match['participants']
#     region = match['subject']['region']

#     for participant in participants:
#         summonerName = participant['summonerName']
#         championId = participant['championId']
#         batch += 1
#         print(
#             f'Match {batch} / {totalBatches}, Time Left: {time_left(batch, totalBatches)}')

#         if (collection.find_one({'summonerName': summonerName})):
#             continue

#         winrate = get_winrates(summonerName, region)
#         collection.insert_one(winrate)


end = time.time()
print(f'Time taken: {end - start} seconds')
