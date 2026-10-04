from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashptstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import CommonTeamRoster
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import teams
import math
import json
import stat_matcher
import pokebase as pb
from flask import jsonify

#nba api stuff:
def create_player (name):
    
    id = locate_id(name)
    
    career = playercareerstats.PlayerCareerStats(player_id = id)

    df = career.get_data_frames()[0] # 0 only refers to all star seasons, change to 4 for full career (view README in nba_api github for more info)
    season = df.iloc[-1]

    #spdStats = leaguedashptstats.LeagueDashPtStats(player_or_team="Player", pt_measure_type="SpeedDistance", per_mode_simple="PerGame", season="2025-26").get_data_frames()[0]

    ppg = round(season["PTS"] / season["GP"], 2)
    apg = round(season["AST"] / season["GP"], 2)
    rpg = round(season["REB"] / season["GP"], 2)
    spg = round(season["STL"] / season["GP"], 2)
    bpg = round(season["BLK"] / season["GP"], 2)
    gp = season["GP"]
    mpg = round(season["MIN"] / season["GP"], 2)
    tpct = season["FG3_PCT"]
    tpa = round(season["FG3A"] / season["GP"], 2)
    rimpct = 54 
    tdef = 36 #default values for these rn since they apparently need to be computed and aren't just available on api
    fgpct = season["FG_PCT"]
    avgspd = 4 #average speed on defense is unreasonably slow so just worry about offense, and temporarily removed

    team = int(season["TEAM_ID"])
    
    info = commonplayerinfo.CommonPlayerInfo(player_id = id)
    player_info = info.get_data_frames()[0]

    position = player_info.iloc[0]["POSITION"]

    # connect this to stat_matcher class after calcs
    return stat_matcher.Player(name, ppg, rpg, apg, spg, bpg, gp, mpg, tpct, tpa, rimpct, tdef, fgpct, avgspd, team, position)
    
def locate_id (name):
    # finds id based off name (i.e. Jokic -> 203999)
    
    ps = players.find_players_by_full_name(name)

    if len(ps) == 1:
        return ps[0]['id']
    else: 
        # some algorithm to let you choose a player if there is more than one with same name
        return None

def locate_name(id):
    return players.find_player_by_id(id)["full_name"]

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

def find_roster(id):

    with open("team_data.json", "r") as f:
        data = json.load(f)

    for i in data:
        if int(i) == id:
            return data[i]
        
    print("If you are seeing this in the terminal, somehow get_roster broke")

def add_roster(id):

    roster = CommonTeamRoster(team_id = id, season = "2025-26")

    players = roster.get_data_frames()[0] #0 is the team roster, 1 is the coach roster apparently

    player_list = []

    for i in range (len(players)):

        player = players.loc[i]
        player_dict = {}

        player_dict["Name"] = player["PLAYER"]
        player_dict["Position"] = player["POSITION"]
        player_dict["PlayerID"] = int(player["PLAYER_ID"])

        player_list.append(player_dict)

    with open("team_data.json", "r") as f:
        data = json.load(f)

    data[id] = player_list #no need to worry about overwiting since this method only runs if data[id] doesn't already exist
    

    with open("team_data.json", "w") as f:
        f.write("\n")
    
        json.dump(data, f, indent = 4)
    


def roster_exists(id):
    with open("team_data.json", "r") as f:
        data = json.load(f)

    for i in data:
        if int(i) == id:
            return True

    return False

def get_roster(id):

    if(roster_exists(id)):
        return find_roster(id)
    else:
        add_roster(id)
        return get_roster(id) #W recursive design?
 
def turn_team_id_to_name(id):
    ts = teams.get_teams()

    for team in ts:
        if team["id"] == id:
            return team["nickname"] #thats what we want fr not no team government name

    return None


def get_player(id):
    name = locate_name(int(id))
    p = create_player(name)

    results = {}

    # all the data that I want to acc display in frontend. other data is incorporated in formulas, but not neccesary in front end
    results ["Name"] = p.name
    results ["PPG"] = p.ppg
    results ["RPG"] = p.rpg
    results ["APG"] = p.apg
    results ["FGPct"] = p.fgPct
    results["TeamID"] = p.team
    results["Team"] = turn_team_id_to_name(p.team)
    results["Position"] = p.position

    results["HP"] = p.hp
    results["ATK"] = p.atk
    results["DEF"] = p.defs
    results["SPCA"] = p.spcA
    results["SPCD"] = p.spcD
    results["SPD"] = p.spd



    return results


def get_dex_num(name):
    return pb.pokemon(name).id #error here with name variable

def get_types(id):
    mon = pb.pokemon(id)
    return mon.types

def get_genus(id):
    return pb.pokemon_species(id).genera[7].genus # 7 is english


#should be ran only once, if you don't already have the files downloaded so they can be created automatically.
#create_kanto_dex_files(pokemon_data.json) 