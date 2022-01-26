from doctest import master
import joblib
from get_data_training import api_calls
from get_data_training import process_data


def predict_last_match(summonerName: str, region: str):
    # Get last match
    match = api_calls.get_past_matches(summonerName, region, 1)[0]
    participants = match['participants']
    print(match['subject']['championId'])

    blueWinrates = []
    blueMasteries = []
    redWinrates = []
    redMasteries = []

    # Get Masteries and Winrates
    for participant in participants:
        championId = participant['championId']
        team = participant['team']

        winrate_list = api_calls.get_winrates(
            participant['summonerName'], region)['winrate']
        mastery_list = api_calls.get_masteries(
            participant['summonerName'], region)['mastery']
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

    # Process Data

    blueData = []
    redData = []

    blueData += process_data.add_data(blueMasteries)
    blueData += process_data.add_data(blueWinrates)
    redData += process_data.add_data(redMasteries)
    redData += process_data.add_data(redWinrates)

    final_data = []
    final_data += blueData
    final_data += redData

    teams = {match['teams'][0]['id']: match['teams'][0]['result'],
             match['teams'][1]['id']: match['teams'][1]['result']}

    if(teams['BLUE'] == 'WON'):
        final_data.append(1)
    else:
        final_data.append(0)

    result = final_data[44]
    dataset = final_data[0:44]

    model = joblib.load('src/finalized_model.sav')

    y_new = model.predict([dataset])
    print(match['subject']['championId'])
    print(y_new)
    print(result)

    return y_new
