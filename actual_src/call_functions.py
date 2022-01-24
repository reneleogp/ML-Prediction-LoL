from bs4 import BeautifulSoup
import requests
import json


def get_past_matches(summonerName: str, region: str, top: int) -> list:
    url = "https://app.mobalytics.gg/api/lol/graphql/v1/query"
    payload = json.dumps({
        "operationName": "LolProfilePageMoreMatchesQuery",
        "variables": {
            "withMatchParticipantDetailed": False,
            "summonerName": summonerName,
            "region": region,
            "top": top,
            "skip": 0,
            "queue": "RANKED_SOLO",
            "rolename": None
        },
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "92fe7bcd15126c52548a71e98d1e16c6fd128692631c73a9b512ea62f072156c"
            }
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    games_list = response.json(
    )['data']['lol']['player']['matchesHistory']['matches']

    return games_list


def get_masteries(summonerName: str, region: str):

    championIds = {'Aatrox': '266', 'Ahri': '103', 'Akali': '84', 'Akshan': '166', 'Alistar': '12', 'Amumu': '32', 'Anivia': '34', 'Annie': '1', 'Aphelios': '523', 'Ashe': '22', 'Aurelion Sol': '136', 'Azir': '268', 'Bard': '432', 'Blitzcrank': '53', 'Brand': '63', 'Braum': '201', 'Caitlyn': '51', 'Camille': '164', 'Cassiopeia': '69', "Cho'Gath": '31', 'Corki': '42', 'Darius': '122', 'Diana': '131', 'Draven': '119', 'Dr. Mundo': '36', 'Ekko': '245', 'Elise': '60', 'Evelynn': '28', 'Ezreal': '81', 'Fiddlesticks': '9', 'Fiora': '114', 'Fizz': '105', 'Galio': '3', 'Gangplank': '41', 'Garen': '86', 'Gnar': '150', 'Gragas': '79', 'Graves': '104', 'Gwen': '887', 'Hecarim': '120', 'Heimerdinger': '74', 'Illaoi': '420', 'Irelia': '39', 'Ivern': '427', 'Janna': '40', 'Jarvan IV': '59', 'Jax': '24', 'Jayce': '126', 'Jhin': '202', 'Jinx': '222', "Kai'Sa": '145', 'Kalista': '429', 'Karma': '43', 'Karthus': '30', 'Kassadin': '38', 'Katarina': '55', 'Kayle': '10', 'Kayn': '141', 'Kennen': '85', "Kha'Zix": '121', 'Kindred': '203', 'Kled': '240', "Kog'Maw": '96', 'LeBlanc': '7', 'Lee Sin': '64', 'Leona': '89', 'Lillia': '876', 'Lissandra': '127', 'Lucian': '236', 'Lulu': '117', 'Lux': '99', 'Malphite': '54', 'Malzahar': '90', 'Maokai': '57', 'Master Yi': '11', 'Miss Fortune': '21', 'Wukong': '62', 'Mordekaiser': '82',
                   'Morgana': '25', 'Nami': '267', 'Nasus': '75', 'Nautilus': '111', 'Neeko': '518', 'Nidalee': '76', 'Nocturne': '56', 'Nunu & Willump': '20', 'Olaf': '2', 'Orianna': '61', 'Ornn': '516', 'Pantheon': '80', 'Poppy': '78', 'Pyke': '555', 'Qiyana': '246', 'Quinn': '133', 'Rakan': '497', 'Rammus': '33', "Rek'Sai": '421', 'Rell': '526', 'Renekton': '58', 'Rengar': '107', 'Riven': '92', 'Rumble': '68', 'Ryze': '13', 'Samira': '360', 'Sejuani': '113', 'Senna': '235', 'Seraphine': '147', 'Sett': '875', 'Shaco': '35', 'Shen': '98', 'Shyvana': '102', 'Singed': '27', 'Sion': '14', 'Sivir': '15', 'Skarner': '72', 'Sona': '37', 'Soraka': '16', 'Swain': '50', 'Sylas': '517', 'Syndra': '134', 'Tahm Kench': '223', 'Taliyah': '163', 'Talon': '91', 'Taric': '44', 'Teemo': '17', 'Thresh': '412', 'Tristana': '18', 'Trundle': '48', 'Tryndamere': '23', 'Twisted Fate': '4', 'Twitch': '29', 'Udyr': '77', 'Urgot': '6', 'Varus': '110', 'Vayne': '67', 'Veigar': '45', "Vel'Koz": '161', 'Vex': '711', 'Vi': '254', 'Viego': '234', 'Viktor': '112', 'Vladimir': '8', 'Volibear': '106', 'Warwick': '19', 'Xayah': '498', 'Xerath': '101', 'Xin Zhao': '5', 'Yasuo': '157', 'Yone': '777', 'Yorick': '83', 'Yuumi': '350', 'Zac': '154', 'Zed': '238', 'Ziggs': '115', 'Zilean': '26', 'Zoe': '142', 'Zyra': '143', 'Zeri': '221'}

    url = f"https://championmastery.gg/summoner?summoner={summonerName}&region={region}"

    response = requests.get(url)

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find("tbody", id="tbody")

        
        job_elements = results.find_all("tr")

        mastery_list = []

        for job_element in job_elements:
            data = []
            data = job_element.text.splitlines()
            championId = int(championIds[data[2]])
            mastery = int(data[4])
            mastery_list.append(
                {
                    'mastery': mastery,
                    'championId': championId
                }
            )

        mastery_dict = {'summonerName': summonerName,
                        'region': region, 'mastery': mastery_list}
        return mastery_dict
    except:
        return None


def get_winrates(summonerName: str, region: str) -> dict:
    url = "https://u.gg/api"
    summonerWinrate = {}
    regionOf = {
        'LAN': 'la1',
        'LAS': 'la2',
        'NA': 'na1',
        'EUW': 'euw1',
        'EUNE': 'eun1',
        'BR': 'br1',
        'JP': 'jp1',
        'KR': 'kr',
        'OCE': 'oc1',
        'RU': 'ru',
        'TR': 'tr1'
    }

    # For season 11
    payload = json.dumps(
        {
            "operationName": "getPlayerStats",
            "variables": {
                "summonerName": summonerName,
                "regionId": regionOf[region],
                "role": 7,
                "seasonId": 17,
                "queueType": [
                    420
                ]
            },
            "query": "query getPlayerStats($queueType: [Int!], $regionId: String!, $role: Int!, $seasonId: Int!, $summonerName: String!) {\n  fetchPlayerStatistics(\n    queueType: $queueType\n    summonerName: $summonerName\n    regionId: $regionId\n    role: $role\n    seasonId: $seasonId\n  ) {\n    basicChampionPerformances {\n      championId\n      totalMatches\n      wins\n      __typename\n    }\n    exodiaUuid\n    puuid\n    queueType\n    regionId\n    role\n    seasonId\n    __typename\n  }\n}\n"
        }
    )

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    playerStats = json.loads(response.text)

    for playerStatistics in playerStats['data']['fetchPlayerStatistics']:
        if playerStatistics['__typename'] == 'PlayerStatistics':
            for championPerformance in playerStatistics['basicChampionPerformances']:
                summonerWinrate[championPerformance['championId']] = dict()
                summonerWinrate[championPerformance['championId']
                                ]['totalMatches'] = championPerformance['totalMatches']
                summonerWinrate[championPerformance['championId']
                                ]['wins'] = championPerformance['wins']

    # For season 12
    payload = json.dumps(
        {
            "operationName": "getPlayerStats",
            "variables": {
                "summonerName": summonerName,
                "regionId": regionOf[region],
                "role": 7,
                "seasonId": 18,
                "queueType": [
                    420
                ]
            },
            "query": "query getPlayerStats($queueType: [Int!], $regionId: String!, $role: Int!, $seasonId: Int!, $summonerName: String!) {\n  fetchPlayerStatistics(\n    queueType: $queueType\n    summonerName: $summonerName\n    regionId: $regionId\n    role: $role\n    seasonId: $seasonId\n  ) {\n    basicChampionPerformances {\n      championId\n      totalMatches\n      wins\n      __typename\n    }\n    exodiaUuid\n    puuid\n    queueType\n    regionId\n    role\n    seasonId\n    __typename\n  }\n}\n"
        }
    )

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    playerStats = json.loads(response.text)

    for playerStatistics in playerStats['data']['fetchPlayerStatistics']:
        if playerStatistics['__typename'] == 'PlayerStatistics':
            for championPerformance in playerStatistics['basicChampionPerformances']:
                if championPerformance['championId'] in summonerWinrate:
                    summonerWinrate[championPerformance['championId']
                                    ]['totalMatches'] += championPerformance['totalMatches']
                    summonerWinrate[championPerformance['championId']
                                    ]['wins'] += championPerformance['wins']
                else:
                    summonerWinrate[championPerformance['championId']] = dict()
                    summonerWinrate[championPerformance['championId']
                                    ]['totalMatches'] = championPerformance['totalMatches']
                    summonerWinrate[championPerformance['championId']
                                    ]['wins'] = championPerformance['wins']

    winrate_list = []

    for championId, champion in summonerWinrate.items():
        winrate_list.append(
            {
                'championID': championId,
                'winrate': (champion['wins'] / champion['totalMatches'] * 100),
            }
        )
    winrate_dict = {'summonerName': summonerName,
                    'region': region, 'winrate': winrate_list}

    return winrate_dict
