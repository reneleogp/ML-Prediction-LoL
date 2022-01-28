import joblib
from api_calls import api_calls
import numpy as np
import scipy.stats
import json


def add_stats(raw_data) -> list:
    processed_data = []

    # add 5 features to the
    processed_data += raw_data

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


""" pip install riotwatcher - https://riot-watcher.readthedocs.io/ """

from riotwatcher import LolWatcher, ApiError
import json

api_key = "RGAPI-c8b616e3-d0f5-47bc-a896-381382dfdc68"
lol_watcher = LolWatcher(api_key)


def get_current_match(region: str, summoner_name: str) -> dict:
    """
    4 requests to Riot API
    If current match does not exist returns None, otherwise returns a dictionary with:

    gameType: str -> The game type
    gameId: int ->  The ID of the game
    participants: list -> The participant information

    The participant information:

    summonerName: str -> The summoner name of this participant
    summonerId: str -> The encrypted summoner ID of this participant
    championId: str -> The ID of the champion played by this participant
    championMastery: int -> Total number of champion points for this player and champion combination
    tier: str -> The player's tier or None if the player has not qualified yet
    rank: str -> The player's division within a tier or None if the player has not qualified yet
    leaguePoints: int -> The player's league points in this tier and rank
    """
    encrypted_summoner_id = lol_watcher.summoner.by_name(region, summoner_name)["id"]

    try:
        current_match = lol_watcher.spectator.by_summoner(region, encrypted_summoner_id)
    except ApiError as e:
        """
        Possible Errors:
            The player is not in match
            Api Key is invalid
        """
        return None
    except:
        """Unexpected Error"""
        return None
    else:
        Dict = dict()

        Dict["gameType"] = current_match["gameType"]
        Dict["gameId"] = current_match["gameId"]
        Dict["gameMode"] = current_match["gameMode"]
        Dict["gameQueueConfigId"] = current_match["gameQueueConfigId"]

        participants = list()
        for participant in current_match["participants"]:
            summoner = dict()

            summoner["summonerName"] = participant["summonerName"]
            summoner["summonerId"] = participant["summonerId"]
            summoner["championId"] = participant["championId"]
            summoner["teamId"] = participant["teamId"]

            summoner["championMastery"] = get_champion_mastery_points(
                region, summoner["summonerId"], summoner["championId"]
            )

            summoner["tier"] = None
            summoner["rank"] = None
            summoner["leaguePoints"] = 0

            league = lol_watcher.league.by_summoner(region, summoner["summonerId"])

            for queue in league:
                if queue["queueType"] == "RANKED_SOLO_5x5":
                    summoner["tier"] = queue["tier"]
                    summoner["rank"] = queue["rank"]
                    summoner["leaguePoints"] = queue["leaguePoints"]

            participants.append(summoner)

        Dict["participants"] = participants

        return Dict


print(json.dumps(get_current_match("la1", "PKS JackeyLove")))


def predict_last_match(summonerName: str, region: str):
    # Get last match

    match = api_calls.get_past_matches(summonerName, region, 1)[0]
    participants = match["participants"]
    print("Match found!")
    blueWinrates = []
    blueMasteries = []
    redWinrates = []
    redMasteries = []

    batch = 0
    totalBatches = 10
    # Get Masteries and Winrates
    for participant in participants:
        batch += 1
        print(f"Processing participant {batch} ({100*batch//totalBatches}%)")
        championId = participant["championId"]
        team = participant["team"]

        winrate_list = api_calls.get_winrates(participant["summonerName"], region)[
            "winrate"
        ]
        mastery_list = api_calls.get_masteries(participant["summonerName"], region)[
            "mastery"
        ]
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

    # Process Data

    print("Processing data...")
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

    result = final_data[44]
    dataset = final_data[0:44]

    model = joblib.load("src/finalized_model.sav")

    prediction = model.predict([dataset])

    response = {}

    with open("champions_name_dictionary.json", "r") as file:
        champions = json.load(file)

    your_championId = match["subject"]["championId"]
    your_team = match["subject"]["team"]
    your_role = match["subject"]["role"]

    response["team"] = your_team
    response["role"] = your_role
    response["champion"] = champions[str(your_championId)]

    if (result == 1 and your_team == "BLUE") or (result == 0 and your_team == "RED"):
        response["won"] = True
    else:
        response["won"] = False

    print(prediction)
    print(result)

    if result == prediction:
        response["correct"] = True
    else:
        response["correct"] = False

    return response


print(predict_last_match("kokkurit", "LAN"))
