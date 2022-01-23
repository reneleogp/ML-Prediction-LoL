from riotwatcher import LolWatcher, ApiError

api_key = "RGAPI-f8cc4077-bd55-4858-a147-6395e463aaed"
lol_watcher = LolWatcher(api_key)


def get_champion_mastery_points(region: str, encrypted_summoner_id: str):

    mastery_points = lol_watcher.champion_mastery.by_summoner(
        region, encrypted_summoner_id)

    return mastery_points


print(get_champion_mastery_points(
    'la1', 'AzX05p8_seUMp3xwp3gPl3lSmLgve_o_Xhp4VHJIy5xRQRt2OpQWUCyCag'))
