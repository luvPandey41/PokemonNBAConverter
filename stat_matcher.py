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


    def find_6_closest(self, pokemon):
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
