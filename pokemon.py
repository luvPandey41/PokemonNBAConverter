import math
import json
import pokebase as pb

class Pokemon:
    def __init__ (self, name, hp, atk, spcA, defs, spcD, spd, id, type1, genus, type2 = None):
        self.name = name

        #remove everything after this
        self.hp = hp
        self.atk = atk
        self.spcA = spcA
        self.defs = defs
        self.spcD = spcD
        self.spd = spd

        self.id = id
        self.type1 = type1
        self.type2 = type2
        self.genus = genus


def create_pokedex_files (num1, num2, fileName):
    # loads pokemon with pokedex numbers from num1 - num2, including both

    data = {} 

    for i in range(num1, num2 + 1): #has to the number of pokemon in the dex + 1, because last value not included
        
        mon = pb.pokemon(i)

        values = {}

        stats = mon.stats
        statList = [stats[0].base_stat, stats[1].base_stat, stats[2].base_stat, stats[3].base_stat, stats[4].base_stat, stats[5].base_stat]

        values["Stats"] = statList
        values["ID"] = i #funny how that works out

        
        try:
            values["Types"] = [mon.types[0].type.name, mon.types[1].type.name]
        except:
            values["Types"] = [mon.types[0].type.name]

        values["Genus"] = mon.species.genera[7].genus # 7 is english

        data[mon.name] = values

        print(mon.name, "is loaded")
    
    with open(fileName, "w") as f:
        json.dump(data, f, indent = 4) # add index = 1 or something if wanted to look different, i didn't because I don't wanna run again


def create_kanto_dex_files (fileName):
    #loading takes multiple minutes, that's why its doesn't make sense to fetch data from api constantly, and file writing is better
    create_pokedex_files(1, 151, fileName)

def convert_file_to_pokemon_object_dict(file):

    results = {}

    with open(file, "r") as f:
        data = json.load(f)
    
    for key in data: 

        
        values = data[key]

        stats = values["Stats"]

        types = values["Types"]

        try:
            temp = Pokemon(key, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], values["ID"], types[0], values["Genus"], type2 = types[1])
        except: 
            temp = Pokemon(key, stats[0], stats[1], stats[2], stats[3], stats[4], stats[5], values["ID"], types[0], values["Genus"])

        results[key] = temp
        
        
    return results


#create_pokedex_files(1, 905, "pokemon_data.json")