import pokemon
import player


#class where all the commands are ran from

def find_pokemons_for_player (playerID):
       return player.get_player(playerID)

def get_roster(teamId):
       return player.get_roster(teamId)

