import math

class Pokemon:
    def __init__ (self, name, hp, atk, spcA, defs, spcD, spd):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.spcA = spcA
        self.defs = defs
        self.spcD = spcD
        self.spd = spd

class Player: 
    # change to nba stat based
    def __init__ (self, name, ppg, rpg, apg, spg, bpg, gp, mpg, tpct, tpa, rimpct, tdef, fgPct, avgSpd):
        
        self.name = name
        self.ppg = ppg
        self.rpg = rpg
        self.apg = apg
        self.bpg = bpg
        self.spg = spg
        self.gp = gp
        self.mpg = mpg
        self.tpct = tpct
        self.tpa = tpa
        self.rimpct = rimpct
        self.avgSpd = avgSpd
        self.tdef = tdef
        self.fgPct = fgPct

        
        self.hp = None
        self.atk = None
        self.spcA = None
        self.defs = None
        self.spcD = None
        self.spd = None

        self.convert_stats()
    
    def convert_stats(self):

        self.hp = math.floor(self.gp * self.mpg / 24)
        self.atk = math.floor(self.ppg * self.fgPct * 8 )
        self.defs = math.floor((self.rpg * 4) + (self.bpg * 12) + (100 - self.rimpct)) #rim percent is the amount a player gets scored on, expressed as a percentage
        self.spcA = math.floor(((self.tpct * self.tpa) * 100) / 4 + self.apg * 4)
        self.spcD = math.floor(self.spg * 12 + (100 - self.tdef)) # tdef is the amount a player gets scored on outside the arc
        self.spd = math.floor(self.avgSpd * 25)


    def find_6_closest(self):
        results = []

        # find the pokemon that are closest to lebron, add ui and changable player later
        for i in pokemon:
            similarity = calculate_similarity(i, self)
            results.append((i.name, similarity))

        #sort the results array based off similarity 
        results.sort(reverse = True, key = lambda x : x[1])

        top6 = []

        for i in range(6):
            top6.append(results[i])

        return top6

def calculate_similarity(pokemon, player):
    # this should later be put into the pokemon class as an object specific method. ok here for now

    Distance =  math.sqrt((pokemon.hp - player.hp) ** 2 + (pokemon.atk - player.atk) ** 2 
                     + (pokemon.spcA - player.spcA) ** 2 + (pokemon.defs - player.defs) ** 2 
                     + (pokemon.spcD - player.spcD) ** 2 + (pokemon.spd - player.spd) ** 2)
    Total = math.sqrt(pokemon.hp ** 2 + pokemon.atk ** 2 + pokemon.spcA ** 2 + pokemon.defs ** 2 + pokemon.spcD ** 2 + pokemon.spd ** 2)
    return round((1 - Distance/Total) * 100, 2)

def findPlayer(n):
    for i in players:
        if i.name == n:
            return i
    print("That player is not in the database")
    return None

lebron = Player("LeBron", 25, 7.5, 8.0, 1.2, .6, 70, 35, 40, 8, 52, 40, 52, 3.2)
giannis = Player("Giannis", 30, 12, 6, 1.2, 1.5, 70, 35, 30, 2, 40, 37, 59, 4.2)
curry = Player("Curry", 27, 5, 6, 1.0, .4, 70, 32, 40, 10, 58, 39, 48, 3.7)
jokic = Player("Jokic", 29, 12, 10, 1.4, .8, 70, 34, 38, 5, 55, 42, 58, 3.5)
luka = Player("Luka", 34, 9, 9, 1.5, .5, 65, 35, 38, 10, 54, 41, 47, 3.6)
wemby = Player("Wemby", 24, 11, 4, 1.0, 3.5, 65, 32, 35, 3, 47, 35, 47, 3.9)
tatum = Player("Tatum", 27, 9, 5, 1.0, .5, 70, 35, 38, 8, 50, 40, 46, 3.8)
embiid = Player("Embiid", 30, 11, 5, 1.0, 1.7, 55, 33, 35, 3, 48, 38, 55, 3.4)
fox = Player("Fox", 26, 4, 6, 1.8, .4, 70, 34, 37, 6, 55, 42, 47, 4.3)
gobert = Player("Gobert", 15, 12, 2, .7, 2.0, 70, 32, 0, 0, 45, 38, 65, 3.4)

players = [lebron, giannis, curry, jokic, luka, wemby, tatum, embiid, fox, gobert] # only use a few of these; the pokemon is what we generally find multiple of.

#flip. Change to getting a player, and showing the closest pokemon to it. its an idea that makes more sense, and is more efficent because you don't have to convert every nba players stats anymore. 

for i in players:
    i.convert_stats()
    # print(i.name, " HP:", i.hp,  " Attack:", i.atk, 
    #    " Special Attack:", i.spcA,  " Defense:",  i.defs,
    #    " Special Defense: ",  i.spcD, " Speed:",  i.spd)

gyarados = Pokemon("Gyarados", 95, 125, 79, 60, 100, 81)

bulbasaur = Pokemon("Bulbasaur", 45, 49, 65, 49, 65, 45)
charmander = Pokemon("Charmander", 39, 52, 60, 43, 50, 65)
squirtle = Pokemon("Squirtle", 44, 48, 50, 65, 64, 43)
pikachu = Pokemon("Pikachu", 35, 55, 50, 40, 50, 90)
raichu = Pokemon("Raichu", 60, 90, 90, 55, 80, 110)
gengar = Pokemon("Gengar", 60, 65, 130, 60, 75, 110)
alakazam = Pokemon("Alakazam", 55, 50, 135, 45, 95, 120)
machamp = Pokemon("Machamp", 90, 130, 65, 80, 85, 55)
golem = Pokemon("Golem", 80, 120, 55, 130, 65, 45)
lapras = Pokemon("Lapras", 130, 85, 85, 80, 95, 60)
dragonite = Pokemon("Dragonite", 91, 134, 100, 95, 100, 80)
tyranitar = Pokemon("Tyranitar", 100, 134, 95, 110, 100, 61)
metagross = Pokemon("Metagross", 80, 135, 95, 130, 90, 70)
mewtwo = Pokemon("Mewtwo", 106, 110, 154, 90, 90, 130)

pokemon = [gyarados, bulbasaur, charmander, squirtle, pikachu, raichu, gengar, alakazam, machamp, golem, lapras, dragonite, tyranitar, metagross, mewtwo]

# the line that decides the player right now
# selected_player = findPlayer("Gobert")

#if selected_player is None:
#    print("Player not found")
#else:
#    top6 = selected_player.find_6_closest()
#
#   for pokemon, similarity in top6:
#       print(pokemon, similarity)