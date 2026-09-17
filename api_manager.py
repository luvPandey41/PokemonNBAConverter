from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashptstats
from nba_api.stats.static import players
import math
import json
import stat_matcher
import pokebase as pb

#nba api stuff:
def create_player (name):
    
    id = locate_id(name)
    
    career = playercareerstats.PlayerCareerStats(player_id = id)
    df = career.get_data_frames()[0] # 0 only refers to all star seasons, change to 4 for full career (view README in nba_api github for more info)
    season = df.iloc[-1]

    #spdStats = leaguedashptstats.LeagueDashPtStats(player_or_team="Player", pt_measure_type="SpeedDistance", per_mode_simple="PerGame", season="2025-26").get_data_frames()[0]

    ppg = round(season["PTS"] / season["GP"])
    apg = round(season["AST"] / season["GP"])
    rpg = round(season["REB"] / season["GP"])
    spg = round(season["STL"] / season["GP"])
    bpg = round(season["BLK"] / season["GP"])
    apg = round(season["REB"] / season["GP"])
    gp = season["GP"]
    mpg = round(season["MIN"] / season["GP"])
    tpct = season["FG3_PCT"]
    tpa = round(season["FG3A"] / season["GP"])
    rimpct = 54 
    tdef = 36 #default values for these rn since they apparently need to be computed and aren't just available on api
    fgpct = season["FG_PCT"]
    avgspd = 4 #average speed on defense is unreasonably slow so just worry about offense, and temporarily removed

    # connect this to stat_matcher class after calcs
    return stat_matcher.Player(name, ppg, rpg, apg, spg, bpg, gp, mpg, tpct, tpa, rimpct, tdef, fgpct, avgspd)
    
def locate_id (name):
    # finds id based off name (i.e. Jokic -> 203999)
    
    ps = players.find_players_by_full_name(name)

    if len(ps) == 1:
        return ps[0]['id']
    else: 
        # some algorithm to let you choose a player if there is more than one with same name
        return None
         

#poke api stuff: 

def load_kanto_dex_files ():
    #loading takes multiple minutes, that's why its doesn't make sense to fetch data from api constantly, and file writing is better
    load_pokedex_files(1, 151)

def load_pokedex_files (num1, num2):
    # loads pokemon with pokedex numbers from num1 - num2, including both

    data = {} 

    for i in range(num1, num2 + 1): #has to the number of pokemon in the dex + 1, because last value not included
        
        temp = pb.pokemon(i)
        stats = temp.stats
        statList = [stats[0].base_stat, stats[1].base_stat, stats[2].base_stat, stats[3].base_stat, stats[4].base_stat, stats[5].base_stat]
       
        data [temp.name] = statList

        print(temp.name, "is loaded")

    #pokedex_as_json = json.dumps(data) 
    #print(poke_as_json)
    
    with open("test.json", "w") as f:
        json.dump(data, f) # add index = 1 or something if wanted to look different, i didn't because I don't wanna run again


def turn_file_to_object():
    pass

#should be ran only once, if you don't already have the files downloaded so they can be created automatically.
#load_kanto_dex_files() 

#print(create_player("Stephen Curry").find_6_closest())

turn_file_to_object()