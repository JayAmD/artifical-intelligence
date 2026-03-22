import numpy as np
import networkx as nx
import random as rnd
from deap import base, creator, tools, algorithms

import matplotlib.pyplot as plt

rnd.seed(64)



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
colors = N

coloredGraphs = []

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

creator.create("Individual", list, fitness=creator.FitnessMin)


toolbox = base.Toolbox()

toolbox.register("attr_int", rnd.randint, 0, colors-1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_int, n=N)


toolbox.register("population", tools.initRepeat, list, toolbox.individual) 



def evaluate(individual):

    collisions = 0
    cols = 0 # number of colors in the current individual
    
    for i in range(N):
        current = individual[i]
        if current+1 > cols:
            cols = current+1
        for j in G.neighbors(i):
            if i < j:
                if current == individual[j]:
                    collisions +=1
    if collisions == 0:
        #global coloredGraphs
        global colors
        coloredGLen = len(coloredGraphs)
        if coloredGLen == 0:
            coloredGraphs.append([colors, individual])
            colors -=1
        elif coloredGraphs[coloredGLen-1][0] > cols:
            coloredGraphs.append([colors, individual])
            colors -=1

    return cols*(collisions+1), # !!!! vracíme n-tici, proto ta čárka
   
   
   # my mutate function
def dynMutate(individual, indpb):
    
    for i in range(len(individual)):
        if rnd.random() < indpb:
            individual[i] = rnd.randint(0,colors-1)
    
    return individual,
   
    
toolbox.register("evaluate", evaluate)


toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", dynMutate, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=2)



NGEN = 20000         # počet generací
CXPB = 0.5           # pravděpodobnost crossoveru na páru
MUTPB = 0.7         # pravděpodobnost mutace


hof = tools.HallOfFame(1)

s = tools.Statistics(key=lambda ind: ind.fitness.values)
s.register("mean", np.mean)
s.register("min", np.min)
s.register("max", np.max)


pop = toolbox.population(n=100)


finalpop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=CXPB, mutpb=MUTPB, ngen=NGEN, stats=s, halloffame=hof)


print('HOF:', hof.keys[0].values)

# plot progress
mean, minimum, maximum = logbook.select("mean", "min", "max")

fig, ax = plt.subplots()

ax.plot(range(NGEN+1), mean, label="mean")     # 0.tá generace zvlášť
ax.plot(range(NGEN+1), minimum, label="min")
ax.plot(range(NGEN+1), maximum, label="max")
ax.legend()