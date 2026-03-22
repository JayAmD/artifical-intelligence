#!/usr/bin/env python
# coding: utf-8

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import math


# Next choose graph
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

G = readdimacs('C:/Users/pavel/Artifical_intelligence/3.Local_search/dsjc125.9.col')  


# Init Coloring
class GraphColoring:
    def color(self, G, colors, maxSteps, seed = 0):
        self.seed = seed
        self.rng = np.random.default_rng(self.seed)
        self.G = G
        self.maxSteps = maxSteps
        self.colors = colors
        self.len = self.G.number_of_nodes()
        
        # beam search
        self.nStates = 20
        self.nSurroundings = 2
        self.state = self.rng.integers(0,self.colors,(self.nStates, self.len), dtype=int)
        self.surroundingState = np.zeros((self.nStates*self.nSurroundings, self.len), dtype=int)
        self.rating = np.zeros(self.nStates*self.nSurroundings, dtype=int) # number of collisions
        self.collisionsLog = np.zeros(maxSteps+1, dtype=int)
        
        # simulated annealing
        self.tempBase = 2.7
        self.temperature = 0
        self.temperatureLog = np.zeros(maxSteps+1, dtype=float)
        
        # low difference
        self.threshold = 0.95
        self.addHeat = 0.02
        self.heatMultiplier = 1
        self.nLastCalls = 10
        self.lastColls = np.zeros(self.nLastCalls, dtype=int)

        self.iterations = 0
        self.solved = self.run()
        return -1, self.solved, self.iterations
    
    
    def run(self): 
        print('Started a run with', self.colors, 'colors.')
        for step in np.arange(self.maxSteps):
            
            # temperature
            self.temperature = 0
            # heat from simulated annealing
            #self.temperature = self.tempBase**(-self.iterations) 
            
            # heat from low differance in between runs
            maxLastColls = np.max(self.lastColls)
            minLastColls = np.min(self.lastColls)
            if minLastColls / maxLastColls > self.threshold:
                print('Adding heat')
                self.temperature += self.addHeat * self.heatMultiplier
                self.heatMultiplier +=1
            else:
                self.heatMultiplier = 1


            # prepare surr
            for i in range(self.nStates):
                for j in range(self.nSurroundings):
                    self.surroundingState[self.nSurroundings*i + j] = np.copy(self.state[i])
                    # Simulated annealing
                    # color some nodes random color, how many nodes depend on the temperature
                    for n in range(self.len):
                        if self.rng.random() < self.temperature:
                            self.surroundingState[self.nSurroundings*i + j, n] = self.rng.integers(0,self.colors)
                    
            self.calculateSurrs()
            self.iterations +=1
            
            # get rating
            for i in range(self.nStates * self.nSurroundings):
                self.rating[i] = self.getRating(self.G, self.surroundingState[i])

            sortedIdx = np.argsort(self.rating)

            # log collisions & temp
            self.collisionsLog[self.iterations] = self.rating[sortedIdx[0]]
            self.temperatureLog[self.iterations] = self.temperature
            
            # log last n colls 
            self.lastColls[self.iterations%self.nLastCalls] = self.rating[sortedIdx[0]]

            print('nCols:',self.colors, 'Iter:', self.iterations, 'Temperature:', round(self.temperature, 3), 'Collisions:', self.rating[sortedIdx[0]])

            # return if graph is correctlly colored
            if self.rating[sortedIdx[0]] == 0:
                return True
          
            # use best surrs as states for the next run
            for i in range(self.nStates):
                self.state[i] = np.copy(self.surroundingState[sortedIdx[i]])
        
        return False
        
    
    def calculateSurrs(self):
        colOccurrence = np.zeros(self.colors, dtype=int)

        for i in range(self.nStates):
            for j in range(self.nSurroundings):
                           
                # iterate nodes in random order
                for idx in self.rng.permutation(self.len):
                    
                    # per algorithm
                    colOccurrence.fill(0)
                    for n in self.G.neighbors(idx):
                        colOccurrence[self.surroundingState[i, n]] +=1
                    minCols = np.where(colOccurrence == colOccurrence.min())
                    newCol = self.rng.choice(minCols[0], 1)
                    self.surroundingState[self.nSurroundings*i + j, idx] = newCol  


    def getRating(self, G, array):
            collisions = 0
            
            for i in range(len(array)):
                for j in G.neighbors(i):
                    if i < j:
                        if array[i] == array[j]:
                            collisions +=1
            return collisions
        
    def plot(self, G, cols): #Draws graphs on top of each other
        k = np.max(cols)
        symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        colmap = ["#"+''.join(self.rng.choice(symbols, 6)) for i in range(k+1)]

        colors = [colmap[c] for c in cols]

        nx.draw(G, node_color=colors, with_labels=True)
    def show(self):
        print('Solved:',self.solved,', Iterations:',self.iterations, 'Difference progress:')
        self.linPlot()
        #self.plot(self.G,self.nodes)
    def linPlot(self):
        fig, ax = plt.subplots()

        #ax.plot([i+1 for i in range(self.iterations)], [0 for i in range(self.iterations)], label='Goal of 0 colls')
        ax.plot([i+1 for i in range(self.iterations)], self.temperatureLog[1:self.iterations+1]*100, label='Temperature')
        ax.plot([i+1 for i in range(self.iterations)], self.collisionsLog[1:self.iterations+1], label= 'Collisons')
        ax.legend()

def findSmallest(class_, G, maxSteps, seed = 0):
    up = G.number_of_nodes()
    low = 0
    mid = 0
    while up - low > 1:
        mid = math.floor((up+low)/2)
        graph = class_()
        cols, solved, iterations = graph.color(G, mid, maxSteps, seed)
        if solved:
            up = mid
        else:
            low = mid
    return up
    
def performance(class_, G, maxColors, maxSteps, cycles):
    iterationsArray = np.empty(cycles, dtype=int)
    for cycle in np.arange(cycles):
        graph = class_()
        cols, solved, iterations = graph.color(G, maxColors, maxSteps, cycle)
        if not solved: #TODO Improve code by not abandoning e.g. increase maxSteps 2x and continue
            print('Abandoned, reached max number of steps in cycle', cycle,'. Incese maxSteps or make sure the graph is colorable with',maxColors,'colors')
            graph.show()
            return 
        iterationsArray[cycle] = iterations
    return np.sum(iterationsArray) / cycles, np.min(iterationsArray), np.max(iterationsArray), iterationsArray

# And choose operation
# --

# In[132]:


graph = GraphColoring()
graph.color(G, 44, 1000)
graph.show()


# In[131]:


findSmallest(GraphColoring, G, 500, )


# In[83]:


performance(GraphColoring, G, 44, 10000, 1000)


# In[90]:


performance(GraphColoring, G, 44, 10000, 1000)


# In[ ]:




