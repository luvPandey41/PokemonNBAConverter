from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashptstats
from nba_api.stats.static import players
import math
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

def load_pokedex ():
    # loads all 151 orginal pokemon. Woudl do 1025 but thats too much
    for i in range(152):
        print(create_pokemon(i+1).name, "is loaded")

def create_pokemon (id): 
    #id is very simple, just equal to the pokedex number
    temp = pb.pokemon(id)
    stats = temp.stats

    return stat_matcher.Pokemon(temp.name, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5])


load_pokedex()
#print(create_player("Stephen Curry").find_6_closest())


