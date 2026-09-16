from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import math


def get_stats (name):

    id = locate_id(name)

    season = get_2026_season(id)
    print("PPG:", round(season["PTS"] / season ["GP"], 2))
    print("APG:", season["AST"] / season ["GP"])
    print("RPG:", season["REB"] / season ["GP"])
    print("SPG:", season["STL"] / season ["GP"])
    print("BPG:", season["BLK"] / season ["GP"])

def get_2026_season (id):
    career = playercareerstats.PlayerCareerStats(player_id = "203999")
    df = career.get_data_frames()[0]
    return df.iloc[-1]

def locate_id (name):
    # finds id based off name (i.e. Jokic -> 203999)
    
    ps = players.find_players_by_full_name(name)

    if len(ps) == 1:
        return ps[0]['id']
    else: 
        # some algorithm to let the player choose
        return None
         
get_stats("LeBron James")