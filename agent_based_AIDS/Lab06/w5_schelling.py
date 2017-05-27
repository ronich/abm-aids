import simpy
import random
from gridplot import GridPlot

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors

white_green_red = matplotlib.colors.ListedColormap(["white", "green", "red"])
plt.register_cmap(cmap=white_green_red)

# color should be a number
class Agent:
    def __init__(self, color, city):
        self.city = city
        self.color = color
        self.loc = self.gen_loc()
        self.city.env.process(self.move())

    def gen_loc(self):
        while True:
            loc = (random.randrange(self.city.city_dim),
                   random.randrange(self.city.city_dim))
            if loc not in self.city.occupied:
                self.city.occupied[loc] = self
                print(self.city.occupied[loc])
                break
                return(loc)

    def pct_similar(self):
        same_color = 0
        neighbors = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx!=0 or dy!=0:
                    ref_loc = ((self.loc[0] + dx) % self.city.city_dim,
                               (self.loc[1] + dy) % self.city.city_dim)
                    if ref_loc in self.city.occupied:
                        neighbors += 1
                        if self.city.occupied[ref_loc].color == self.color:
                            same_color += 1
        return(1 if neighbors == 0 else same_color / neighbors)

    def is_happy(self):
        return(self.pct_similar() >= self.city.similar_wanted)

    def move(self):
        yield self.city.env.timeout(random.random())
        while True:
            yield self.city.env.timeout(1)
            if not self.is_happy():
                new_loc = self.gen_loc()
                del self.city.occupied[self.loc]
                self.loc = new_loc

class City:
    def __init__(self, city_dim, similar_wanted, density, max_iter):
        self.city_dim = city_dim
        self.similar_wanted = similar_wanted
        self.density = density
        self.max_iter = max_iter

    def all_happy(self):
        while True:            
            if self.env.now > self.max_iter:
                self.finish_event.succeed()
            yield self.env.timeout(1)
            for v in self.occupied.values():
                if not v.is_happy():
                    break
            else:
                self.finish_event.succeed()

    def plot(self):
        self.data = np.zeros((self.city_dim, self.city_dim))
        for agent in self.occupied:
            self.data[agent] = self.occupied[agent].color
        self.gp = GridPlot(self.data, ["white", "green", "red"])
        while True:
            yield self.env.timeout(.025)
            self.gp.plot()

    def run(self):
        self.occupied = dict()
        self.env = simpy.Environment()
        agent_count = int(self.city_dim * self.city_dim * self.density / 2)
        for i in range(agent_count):
            Agent(1, self)
        for i in range(agent_count):
            Agent(2, self)
        for i in range(agent_count):
            Agent(3, self)
        self.finish_event = self.env.event()
        self.env.process(self.plot())
        self.env.process(self.all_happy())                
        self.env.run(until=self.finish_event)
        #sum_ih = sum([v.is_happy() for v in self.occupied.values()])
        #sum_ps = sum([v.pct_similar() for v in self.occupied.values()])
        #return(self.env.now,
        #       sum_ih / len(self.occupied),
        #       sum_ps / len(self.occupied))

city = City(10, 0.1, 0.8, 50)
city.run()
