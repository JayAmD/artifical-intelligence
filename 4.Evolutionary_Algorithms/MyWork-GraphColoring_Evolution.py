import numpy as np
import networkx as nx
import random as rnd
from deap import base, creator, tools, algorithms

import matplotlib.pyplot as plt

rnd.seed(64)

colors = 5

# read graph
G = nx.Graph()


def readdimacs(filename):

    file = open(filename, 'r')
    lines = file.readlines()
    
    Gd = nx.Graph()

    for line in lines:
        if line[0] == "e":
            vs = [int(s) for s in line.split() if s.isdigit()]
            Gd.add_edge(vs[0]-1, vs[1]-1)
    return Gd

G = readdimacs('C:/Users/pavel/Artifical_intelligence/4.Evolutionary_Algorithms/dsjc125.1.col')  


N = G.number_of_nodes() # number nodes

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

creator.create("Individual", list, fitness=creator.FitnessMin)


toolbox = base.Toolbox()

toolbox.register("attr_int", rnd.randint, 0, colors-1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_int, n=N)


toolbox.register("population", tools.initRepeat, list, toolbox.individual) 



def evaluate(individual):

    collisions = 0
    
    for i in range(N):
        for j in G.neighbors(i):
            if i < j:
                if individual[i] == individual[j]:
                    collisions +=1

    return collisions, # !!!! vracíme n-tici, proto ta čárka
   
   

   
    
toolbox.register("evaluate", evaluate)


toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt, low =0, up =colors-1, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=2)



NGEN = 10000         # počet generací
CXPB = 0.5           # pravděpodobnost crossoveru na páru
MUTPB = 0.7         # pravděpodobnost mutace


hof = tools.HallOfFame(1)

s = tools.Statistics(key=lambda ind: ind.fitness.values)
s.register("mean", np.mean)
s.register("min", np.min)


pop = toolbox.population(n=100)


finalpop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=s, halloffame=hof)


print('HOF:', hof.keys[0].values)

# plot progress
mean, minimum = logbook.select("mean", "min")

fig, ax = plt.subplots()

ax.plot(range(NGEN+1), mean, label="mean")     # 0.tá generace zvlášť
ax.plot(range(NGEN+1), minimum, label="min")
ax.legend()