from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import CommonTeamRoster
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import teams
from nba_api.stats.endpoints import LeagueDashPtStats
from nba_api.stats.endpoints import LeagueDashPtDefend
import math
import pokemon
import json

class Player:
    def __init__(self, name):
        (self.name, self.ppg, self.rpg, self.apg, self.spg, self.bpg, self.gp, self.mpg, self.tpct, self.tpa, self.rimpct, self.tdef, 
         self.fgPct, self.avgSpd, self.team, self.position) = self.create_player(name)

        self.hp = None
        self.atk = None
        self.spcA = None
        self.defs = None
        self.spcD = None
        self.spd = None

        self.convert_stats()

        self.six_closest = self.find_6_closest()


    @staticmethod
    def create_player(name):
        player_id = locate_id(name)

        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        df = career.get_data_frames()[0]
        season = df.iloc[-1]

        gp = season["GP"]

        ppg = round(season["PTS"] / gp, 2)
        apg = round(season["AST"] / gp, 2)
        rpg = round(season["REB"] / gp, 2)
        spg = round(season["STL"] / gp, 2)
        bpg = round(season["BLK"] / gp, 2)
        mpg = round(season["MIN"] / gp, 2)
        tpct = season["FG3_PCT"]
        tpa = round(season["FG3A"] / gp, 2)

        rimpct, tdef = get_defensive_stats(player_id)
        
        fgPct = season["FG_PCT"]
        avgSpd = get_avg_speed(player_id)

        team = int(season["TEAM_ID"])

        info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        player_info = info.get_data_frames()[0]
        position = player_info.iloc[0]["POSITION"]

        return (name, ppg, rpg, apg, spg, bpg, gp, mpg, tpct, tpa, rimpct, tdef, fgPct, avgSpd, team, position)

    def convert_stats(self):
        self.hp = math.floor(40 + (self.gp * self.mpg / 30))
        self.atk = math.floor(40 + self.ppg * self.fgPct * 6 )
        self.defs = math.floor(55 + self.rpg * 3 + self.bpg * 10+ (0.55 - self.rimpct) * 120) #rim percent is the amount a player gets scored on, expressed as a percentage
        self.spcA = math.floor(35 + (self.tpct * self.tpa * 15)  + self.apg * 4)
        self.spcD = math.floor(65 + self.spg * 6 + (0.36 - self.tdef) * 130) # tdef is the amount a player gets scored on outside the arc
        self.spd = math.floor(40 + self.avgSpd * 8)

    def calculate_similarity(self, pokemon):
        distance = math.sqrt(
            (pokemon.hp - self.hp) ** 2 + (pokemon.atk - self.atk) ** 2 + (pokemon.spcA - self.spcA) ** 2 + (pokemon.defs - self.defs) ** 2
            + (pokemon.spcD - self.spcD) ** 2 + (pokemon.spd - self.spd) ** 2)

        total = math.sqrt(pokemon.hp ** 2 + pokemon.atk ** 2 + pokemon.spcA ** 2 + pokemon.defs ** 2 + pokemon.spcD ** 2 + pokemon.spd ** 2)

        return round((1 - distance / total) * 100, 2)


    def find_6_closest(self):

        pokemons = pokemon.convert_file_to_pokemon_object_dict("pokemon_data.json")

        results = []

        for key in pokemons:
            mon = pokemons[key]
            similarity = self.calculate_similarity(mon)
            results.append((mon, similarity)) 

        #sort the results array based off similarity 
        results.sort(reverse = True, key = lambda x : x[1])

        top6 = []

        for i in range(6):
            current = {}

            mon, similarity = results[i]

            current["similarity"] = float(similarity)

            pokemonDict = {"name": mon.name, "hp": int(mon.hp), "atk": int(mon.atk), "spcA": int(mon.spcA), "defs": int(mon.defs),
                    "spcD": int(mon.spcD), "spd": int(mon.spd), "id": int(mon.id), "type1": mon.type1, "type2": mon.type2, "genus": mon.genus,}

            current["pokemon"] = pokemonDict

            top6.append(current)
            
        return top6
    

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
    p = Player(name)

    results = {"name": p.name, "ppg": float(p.ppg), "rpg": float(p.rpg), "apg": float(p.apg), "spg": float(p.spg), "bpg": float(p.bpg),
    "gp": int(p.gp), "mpg": float(p.mpg), "tpct": float(p.tpct), "tpa": float(p.tpa), "rimpct": float(p.rimpct), "tdef": float(p.tdef),
    "fgPct": float(p.fgPct), "avgSpd": float(p.avgSpd), "team": int(p.team), "teamName": turn_team_id_to_name(int(p.team)),
    "position": p.position, "hp": int(p.hp), "atk": int(p.atk), "spcA": int(p.spcA), "defs": int(p.defs), "spcD": int(p.spcD),
    "spd": int(p.spd), "six_closest": p.six_closest}   
    
    return results

def get_avg_speed(player_id):
    tracking = LeagueDashPtStats(season= "2025-26", pt_measure_type= "SpeedDistance", player_or_team="Player")

    df = tracking.get_data_frames()[0]

    player = df[df["PLAYER_ID"] == player_id] #the way you actually individualize the data to the player with id player_id

    return player.iloc[0]["AVG_SPEED"]

def get_defensive_stats(player_id):

    response = LeagueDashPtDefend(season = "2025-26", defense_category = "2 Pointers")
    df = response.get_data_frames()[0]
    player = df[df["CLOSE_DEF_PERSON_ID"] ==  player_id]
    FG2_PCT = player.iloc[0]["FG2_PCT"]

    response = LeagueDashPtDefend(season = "2025-26", defense_category = "3 Pointers")
    df = response.get_data_frames()[0]
    player = df[df["CLOSE_DEF_PERSON_ID"] ==  player_id]
    FG3_PCT = player.iloc[0]["FG3_PCT"]
                                  
    return FG2_PCT, FG3_PCT
