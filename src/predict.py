import json
import re
import joblib
from api_calls import api_calls
import numpy as np
import scipy.stats

with open("champions_name_dictionary.json", "r") as file:
    champions = json.load(file)


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


def predict_match(match, region):
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
        summonerName = participant["summonerName"]

        winrate_list = api_calls.get_winrates(summonerName, region)["winrate"]
        mastery_list = api_calls.get_masteries(summonerName, region)["mastery"]
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

    dataset = final_data
    model = joblib.load("src/finalized_model.sav")
    prediction = model.predict([dataset])

    return prediction


def get_current_match_prediction(summonerName: str, region: str):
    print("-----Getting current match-----")
    region1 = region
    regionOf = {
        "LAN": "la1",
        "LAS": "la2",
        "NA": "na1",
        "EUW": "euw1",
        "EUNE": "eun1",
        "BR": "br1",
        "JP": "jp1",
        "KR": "kr",
        "OCE": "oc1",
        "RU": "ru",
        "TR": "tr1",
    }
    region = regionOf[region]

    match = dict()
    match = api_calls.get_live_match(summonerName, region)

    if match == None:
        return None

    for participant in match["participants"]:
        if participant["summonerName"] == summonerName:
            your_team = participant["team"]
            your_champion = champions[str(participant["championId"])]
            your_role = participant["currentRole"]

    response = {}
    prediction = predict_match(match, region1)
    print(f"Prediction: {prediction}")
    if (prediction == 1 and your_team == "BLUE") or (
        prediction == 0 and your_team == "RED"
    ):
        response["victory_predicted"] = True
    else:
        response["victory_predicted"] = False

    response["team"] = your_team
    response["champion"] = your_champion
    response["role"] = your_role

    return response


def get_last_match_prediction(summonerName: str, region: str):
    # Get last match
    print("-----Getting last match-----")
    match = api_calls.get_past_matches(summonerName, region, 1)[0]
    prediction = predict_match(match, region)

    teams_result = {
        match["teams"][0]["id"]: match["teams"][0]["result"],
        match["teams"][1]["id"]: match["teams"][1]["result"],
    }

    if teams_result["BLUE"] == "WON":
        result = 1
    else:
        result = 0

    response = {}

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

    print(f"Prediction: {prediction}")
    print(f"Result: {result}")

    if result == prediction:
        response["correct"] = True
    else:
        response["correct"] = False

    return response
