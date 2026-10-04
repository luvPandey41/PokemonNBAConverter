import api_manager
import stat_matcher


#class where all the commands are ran from

def find_pokemons_for_player (playerID):
       p = api_manager.create_player(api_manager.locate_name(playerID))
       
       mons = []
       mons = api_manager.turn_file_to_object("pokemon_data.json") # render all 151 pokemon

       return p.find_6_closest(mons)

def prompt():
       #print("Enter your player: ") 
       id = 2544 #input
       return find_pokemons_for_player(id)

       #print(results)

def get_roster(teamId):
       return api_manager.get_roster(teamId)

def get_player(playerID):
       return api_manager.get_player(playerID)


#prompt()