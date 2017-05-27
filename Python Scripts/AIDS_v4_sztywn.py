# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:06:03 2015

@author: Roni
"""
# 0. Import bibliotek

import random as rnd
import numpy as np
import matplotlib.pyplot as plt

#%%

#1. Ustalenie charakterystyk i ziarna losowego

"""MAX_ITER = 500     # Max number of iterations
N = 100            # Number of people"""
INF_PCT = 0.05      # Initial percentage of infected people
CPL_TEND = 0.20     # Average coupling tendency
COMMIT = 50         # Average commitment [weeks]
"""CCEPT_USE = 0.05    # Average chance of using protection
TEST_FREQ = 0.08    # Average number of tests taken by one person per year"""
INF_CHANCE = 0.5    # Chance of passing on an infection

"""rnd.seed(RANDOM_SEED)"""
#%%

#2. Definicja agenta, nadanie mu cech
class Agent:
    
    def __init__(self, ID, society):
        self.ID = ID
        self.society = society
        self.righty = True if rnd.random() > 0.5 else False
        self.inf = True if len(self.society.people) < INF_PCT*society.population else False
        self.inf_len = 0
        self.known = False
        self.cpl_len = 0
        self.partner = None
        self.cpl_tend = CPL_TEND
        #self.cpl_tend = rnd.normalvariate(CPL_TEND, CPL_TEND/2)
        self.commit = COMMIT
        #self.commit = int(rnd.normalvariate(COMMIT, COMMIT/2))
        self.ccept_use = society.ccept_use
        self.test_freq = society.test_freq
        self.INF_CHANCE = INF_CHANCE
        
        self.society.people[self.ID] = self

    def coupling(self):
        while self.partner == None and self.righty == True:
            chosen = rnd.randint(0, len(self.society.people)-1)
            if rnd.random() > 0.1:
                break
            if self.society.people[chosen].righty == True or self.society.people[chosen].partner != None:
                continue
            if rnd.random() > np.mean([self.cpl_tend, self.society.people[chosen].cpl_tend]):
                break
            self.partner = self.society.people[chosen]
            self.partner.partner = self
            break

    def relationship(self):
        if self.partner != None:
            self.cpl_len += 1
            if ((self.inf == True or self.partner.inf == True)
                and (self.known != True and self.partner.known != True)
                and rnd.random() > np.mean([self.ccept_use, self.partner.ccept_use])
                and rnd.random() <= self.INF_CHANCE):
                self.inf = True
                self.partner.inf = True                        
            if min(self.cpl_len, self.partner.cpl_len) > self.commit:
                self.cpl_len = 0
                self.partner.cpl_len = 0
                self.partner.partner = None
                self.partner = None
            
    def testing(self):
        self.inf_len += 1 if self.inf == True else 0
        if self.known == True:
            return None
        self.known = True if self.inf == True and (rnd.random() <= (self.test_freq/52) or (self.inf_len >= 200 and rnd.random() < 0.01)) else False

class Society:
    
    def __init__(self, population, max_iter, CCEPT_USE, TEST_FREQ):
        self.population = population
        self.max_iter = max_iter
        self.ccept_use = CCEPT_USE
        self.test_freq = TEST_FREQ
        self.time = 0
    
    def plot(self, y, label, loc, col, fin = False):
        plt.axis([0, self.time, 0, 100])
        x=list(range(0, self.time))
        plotline = plt.plot(y, label = label, color = col)
        legend_to_add = plt.legend(plotline, label, loc = loc)
        plt.gca().add_artist(legend_to_add)
        plt.scatter(x, y)
        plt.draw()
        if fin == True:
            plt.show()
        
    """ To jest funkcja do plotowania interaktywnego - na razie niepotrzebna  
    def plot_int(self, y, label, loc, col):
        plt.axis([0, self.max_iter, 0, self.population])
        plt.ion()
        x=list(range(0, self.time))
        plotline = plt.plot(y, label = label, color = col)
        legend_to_add = plt.legend(plotline, label, loc)
        plt.gca().add_artist(legend_to_add)
        plt.scatter(x, y)
        plt.draw()
        plt.show()
        time.sleep(0.005)
    """
    
    def run(self):
        self.people = dict()
        for i in range(self.population):
            Agent(i, self)
        self.hivn_cnt = list()
        self.hivu_cnt = list()
        self.hivp_cnt = list()
        while self.time <= self.max_iter:
            self.time += 1
            self.hivn_num = 0
            self.hivu_num = 0
            self.hivp_num = 0
            for i in self.people:
                self.people[i].coupling()
                self.people[i].relationship()
                self.people[i].testing()
            for i in self.people:
                self.hivn_num += 1 if self.people[i].inf == False else 0
                self.hivu_num += 1 if self.people[i].inf == True and self.people[i].known == False else 0
                self.hivp_num += 1 if self.people[i].known == True else 0
            self.hivn_cnt.append(int(self.hivn_num))
            self.hivu_cnt.append(self.hivu_num)
            self.hivp_cnt.append(self.hivp_num)
            if self.hivu_num == 0:
                break
            """self.plot_int(self.couples_cnt, 'Couples', 2, 'b')
            self.plot_int(self.inf_cnt, 'Infected', 9, 'g')
            self.plot_int(self.known_cnt, 'Known-Infected', 1, 'r')  """  
        """self.plot(self.hivn_cnt, ('HIV-',), 2, 'b')
        self.plot(self.hivu_cnt, ('HIV?',), 9, 'g')
        self.plot(self.hivp_cnt, ('HIV+',), 1, 'r', True)"""
        return (self.time, float(self.hivp_num)/float(self.population))
        
#%%
            
def Metamodel(points, reps, N, MAX_ITER, RANDOM_SEED):
    
    with open("aids_output.txt", "w") as fh:
        
        rnd.seed(RANDOM_SEED)
        
        for point in range(points):
            CCEPT_USE = rnd.uniform(0,1)
            TEST_FREQ = rnd.uniform(0,1)
            for rep in range(reps):
                soc = Society(N, MAX_ITER, CCEPT_USE, TEST_FREQ).run()
                values = list(map(lambda x: str(x), [point, rep, CCEPT_USE, TEST_FREQ, soc[0], soc[1]]))
                print(";".join(values))
                fh.write(";".join(values)+'\n')
            
#%%
Metamodel(300, 3, 500, 100, 42)