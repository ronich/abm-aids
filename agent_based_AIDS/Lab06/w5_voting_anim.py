import simpy
import random
import math

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors
from gridplot import GridPlot

white_green_red = matplotlib.colors.ListedColormap(["white",
                                                    "green",
                                                    "red",
                                                    "blue"])
plt.register_cmap(cmap=white_green_red)

# color should be a number
class Agent:
    def __init__(self, color, city):
        self.city = city
        self.color = color
        self.city.env.process(self.move())
        while True:
            self.loc = (random.randrange(self.city.city_dim),
                        random.randrange(self.city.city_dim))
            if self.loc not in self.city.occupied:
                self.city.occupied[self.loc] = self
                break

    def update(self):
        neighbors = dict()
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                ref_loc = ((self.loc[0] + dx) % self.city.city_dim,
                           (self.loc[1] + dy) % self.city.city_dim)
                if ref_loc in self.city.occupied:
                    nei_color = self.city.occupied[ref_loc].color
                    neighbors[nei_color] = neighbors.get(nei_color, 0) + 1
        max_nei = max(neighbors.values())
        considered = list()
        for k in neighbors:
            if neighbors[k] == max_nei:
                considered.append(k)
        self.color = random.choice(considered)
        self.city.data[self.loc] = self.color

    def move(self):
        while True:
            wait = math.ceil(self.city.env.now) - self.city.env.now
            yield self.city.env.timeout(wait + random.random())
            self.update()

class City:
    def __init__(self, city_dim, density,    max_iter):
        self.city_dim = city_dim
        self.density = density
        self.max_iter = max_iter

    def plot(self):
        self.data = np.zeros((self.city_dim, self.city_dim))
        for agent in self.occupied:
            self.data[agent] = self.occupied[agent].color
        self.gp = GridPlot(self.data, ["white", "green", "red", "blue"])
        while True:
            yield self.env.timeout(.025)
            self.gp.plot()
            
    def run(self):
        self.occupied = dict()
        self.env = simpy.Environment()
        agent_count = int(self.city_dim * self.city_dim * self.density / 3.2)
        for i in range(agent_count):
            Agent(1, self)
        for i in range(agent_count):
            Agent(2, self)
        for i in range(agent_count):
            Agent(3, self)
        self.env.process(self.plot())
        self.env.run(until=self.max_iter)

city = City(51, 1, 10)
city.run()
