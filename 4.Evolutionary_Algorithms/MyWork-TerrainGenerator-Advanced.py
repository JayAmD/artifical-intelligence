import numpy as np

import random as rnd

from deap import base, creator, tools, algorithms

import matplotlib.pyplot as plt


goal = {
    'waterPct': 0.4, # % of water tiles
    
    'smIsldLen': [2,4], # lenght 2-4
    'smIsldPct': 0.4 # % of small island tiles
    }

N = 100 # number of points of the terrain


creator.create("FitnessMax", base.Fitness, weights=(1.0,))

creator.create("Individual", list, fitness=creator.FitnessMax)


toolbox = base.Toolbox()

toolbox.register("attr_float", rnd.random)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=N)


toolbox.register("population", tools.initRepeat, list, toolbox.individual) 



def evaluate(individual):

    isldLen = 0
    #smIslds = []
    nSmIsldTile = 0
    nWater = 0
    
    for i in range(N):
        if individual[i] >= 0.5:
            isldLen +=1
        else:
            if goal['smIsldLen'][0] <= isldLen <= goal['smIsldLen'][1]:
                #smIslds.append(isldLen)
                nSmIsldTile += isldLen
            isldLen = 0
            nWater +=1

    waterPct = nWater / N
    waterRealToGoal = waterPct / goal['waterPct']
    
    smIsldPct = nSmIsldTile / N
    smIsldRealToGoal = smIsldPct / goal['smIsldPct']
    
    # evaluation
    score = (waterRealToGoal*0.5 + smIsldRealToGoal*0.5)*100
    return score, # !!!! vracíme n-tici, proto ta čárka
   
   
def mutateFloat(individual, indpb):
    
    for i in range(len(individual)):
        if rnd.random() < indpb:
            individual[i] = rnd.random()
    
    return individual,
   
    
toolbox.register("evaluate", evaluate)


toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mutateFloat, indpb=0.01)
toolbox.register("select", tools.selRoulette)



NGEN = 1000         # počet generací
CXPB = 0.5           # pravděpodobnost crossoveru na páru
MUTPB = 0.7         # pravděpodobnost mutace



s = tools.Statistics(key=lambda ind: ind.fitness.values)
s.register("mean", np.mean)
s.register("max", np.max)

hof = tools.HallOfFame(1)

pop = toolbox.population(n=100)


finalpop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=s, halloffame=hof)


# plot terrain
fig, ax = plt.subplots()
     
ax.plot(range(N), [0.5 for i in range(100)], label="water level")
ax.plot(range(N), hof[0], marker=".", label="sand")
ax.axis([0, 100, -4, 5])
ax.legend()

# plot progress
mean, maximum = logbook.select("mean", "max")

fig, ax = plt.subplots()

ax.plot(range(NGEN+1), mean, label="mean")     # 0.tá generace zvlášť
ax.plot(range(NGEN+1), maximum, label="max")
ax.legend()