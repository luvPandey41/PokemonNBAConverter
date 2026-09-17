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

def create_kanto_dex_files (fileName):
    #loading takes multiple minutes, that's why its doesn't make sense to fetch data from api constantly, and file writing is better
    create_pokedex_files(1, 151, fileName = "kanto")

def create_pokedex_files (num1, num2, fileName):
    # loads pokemon with pokedex numbers from num1 - num2, including both

    data = {} 

    for i in range(num1, num2 + 1): #has to the number of pokemon in the dex + 1, because last value not included
        
        temp = pb.pokemon(i)
        stats = temp.stats
        statList = [stats[0].base_stat, stats[1].base_stat, stats[2].base_stat, stats[3].base_stat, stats[4].base_stat, stats[5].base_stat]
       
        data [temp.name] = statList

        print(temp.name, "is loaded")
    
    with open(fileName, "w") as f:
        json.dump(data, f) # add index = 1 or something if wanted to look different, i didn't because I don't wanna run again


def turn_file_to_object(file):

    result = []

    with open(file, "r") as f:
        data = json.load(f)
    
    for i in data: 
        statList = data[i]
        temp = stat_matcher.Pokemon(i, statList[0], statList[1], statList[2], statList[3], statList[4], statList[5])
        result.append(temp)
        
    return result
    

#should be ran only once, if you don't already have the files downloaded so they can be created automatically.
#create_kanto_dex_files() 