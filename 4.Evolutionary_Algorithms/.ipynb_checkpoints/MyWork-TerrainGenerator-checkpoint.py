import numpy as np

import random as rnd

from deap import base, creator, tools, algorithms

import matplotlib.pyplot as plt


target = 70 # target lenght of island, island has a water tile from left, but may not have water tile from right

N = 100 # number of points of the terrain


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

creator.create("Individual", list, fitness=creator.FitnessMin)


toolbox = base.Toolbox()

toolbox.register("attr_float", rnd.random)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=N)


toolbox.register("population", tools.initRepeat, list, toolbox.individual) 


# retunrs number of island tiles not to specifications
def evaluate(individual):

    firstWaterTile = False
    islandTiles = 0
    longestIsland = 0
    
    # messurament
    for tile in range(N):
        if islandTiles == 0 and individual[tile] < 0.5:
            firstWaterTile = True
        elif firstWaterTile and individual[tile] >= 0.5:
            islandTiles +=1
        else:
            islandTiles = 0
            
        if islandTiles > longestIsland:
            longestIsland = islandTiles

    # evaluation
    score = abs(longestIsland - target)
    
    return score, # !!!! vracíme n-tici, proto ta čárka
   
    
toolbox.register("evaluate", evaluate)


toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=1, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=2)



NGEN = 10000         # počet generací
CXPB = 0.5           # pravděpodobnost crossoveru na páru
MUTPB = 0.7         # pravděpodobnost mutace



s = tools.Statistics(key=lambda ind: ind.fitness.values)
s.register("mean", np.mean)
s.register("min", np.min)


pop = toolbox.population(n=100)


finalpop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=s)

#%%
# plot
mean, minimum = logbook.select("mean", "min")

fig, ax = plt.subplots()

ax.plot(range(NGEN+1), mean, label="mean")     # 0.tá generace zvlášť
ax.plot(range(NGEN+1), minimum, label="min")
ax.legend()