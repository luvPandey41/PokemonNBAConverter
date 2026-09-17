import api_manager
import stat_matcher


#class where all the commands are ran from

# request player --> fetch player data from api --> create player with that data --> 
# fetch pokemon data from api --> create kanto pokeomn with that data --> 
# calculate similarity with all 151 kanto pokemon --> return the top 6 most similar pokemon, with their percentages

print("Enter your player: ") 
name = input()

p = api_manager.create_player(name) #make the player object by the name of whatever was inputed

mons = []
mons = api_manager.turn_file_to_object("test.json") # render all 151 pokemon

top6 = p.find_6_closest(mons)

for pokemon, similarity in top6:
       print(pokemon, similarity)
