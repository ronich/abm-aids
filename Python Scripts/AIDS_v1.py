# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 20:06:03 2015

@author: Roni
"""
# 0. Import bibliotek

import random as rnd
import numpy as np
import matplotlib.pyplot as plt
import time

#%%

#1. Ustalenie charakterystyk i ziarna losowego

RANDOM_SEED = 42
MAX_ITER = 500     # Max number of iterations
N = 100            # Number of people
INF_PCT = 0.05      # Initial percentage of infected people
CPL_TEND = 0.05     # Average coupling tendency
COMMIT = 50         # Average commitment [weeks]
CCEPT_USE = 0.05    # Average chance of using protection
TEST_FREQ = 0.1    # Average number of tests taken by one person per year
INF_CHANCE = 0.5    # Chance of passing on an infection

rnd.seed(RANDOM_SEED)
#%%

#2. Definicja agenta, nadanie mu cech
class Agent:
    
    def __init__(self, ID, society):
        self.ID = ID # jego ID
        self.society = society # społeczeństwo, do ktorego nalezy
        self.righty = True if rnd.random() > 0.5 else False # tak jak w netlogo, righty = inicjator kontaktu
        self.inf = True if len(self.society.people) < INF_PCT*N else False # czy jest zainfekowany na start
        self.inf_len = 0 # długość infekcji
        self.known = False # czy wie o infekcji
        self.cpl_len = 0 # długość związku
        self.partner = None # kto jest jego partnerem
        self.cpl_tend = CPL_TEND
        self.commit = COMMIT
        self.ccept_use = CCEPT_USE
        self.test_freq = TEST_FREQ
        self.INF_CHANCE = INF_CHANCE
        
        self.society.people[self.ID] = self # dołączenie go do społeczeństwa (słownik)

    def coupling(self):
        # funkcja łączenia się w pary
        while self.partner == None and self.righty == True: # wolny i inicjator
            chosen = rnd.randint(0, len(self.society.people)-1) # wybrany "cel"
            if rnd.random() > 0.1: # prawdopodobieństwo zainicjowania kontaktu - nad tym trzeba się jeszcze zastanowić
                break
            if self.society.people[chosen].righty == True or self.society.people[chosen].partner != None: # sprawdzamy, czy wybranek(ka) nie jest też right i czy nie ma partnera            
                continue # jeżeli tak, wybieramy kogoś innego
            if rnd.random() > np.mean([self.cpl_tend, self.society.people[chosen].cpl_tend]):
                break # jeżeli nie ("cel" jest ok), ale nie dojdzie do wejścia w związek, wychodzimy z pętli
            self.partner = self.society.people[chosen] # jeżeli powyższe się nie zadzieją - wchodzimy w związek
            self.partner.partner = self
            #print('%s Found a girl! Chosen one: %s' % (self.ID, self.partner.ID))
            break

    def relationship(self):
        # funkcja związku
        if self.partner != None: #tylko dla tych, ktorzy są w związku
            self.cpl_len += 1
            if ((self.inf == True or self.partner.inf == True)
                and (self.known != True and self.partner.known != True)
                and rnd.random() > np.mean([self.ccept_use, self.partner.ccept_use])
                and rnd.random() <= self.INF_CHANCE): # sprawdzamy zestaw warunkow, ktore musza byc spelnione zeby zarazic partnera HIV
                self.inf = True
                self.partner.inf = True                        
            if min(self.cpl_len, self.partner.cpl_len) > self.commit: # tutaj ze soba zrywamy, jezeli nadszedl czas konca zwiazku
                #print('%s broke up with %s!' % (self.ID, self.partner.ID))
                self.cpl_len = 0
                self.partner.cpl_len = 0
                self.partner.partner = None
                self.partner = None
            
    def testing(self):
        # funkcja badania się na obecność wirusa
        self.inf_len += 1 if self.inf == True else 0
        if self.known == True:
            return None
        self.known = True if self.inf == True and (rnd.random() <= (TEST_FREQ/52) or (self.inf_len >= 200 and rnd.random() < 0.05)) else False
        # Agent dowie się, że jest zarażony albo bo sam pjdzie albo bo minie określona liczba okresow i (moze) wystapia symptomy

# Inicjujemy klasę społeczeństwo
class Society:
    
    def __init__(self, population, max_iter):
        self.population = population
        self.max_iter = max_iter
        self.time = 0
    
    def plot(self, y, label, loc, col):
        #funkcja do plotowania wynikow
        plt.axis([0, self.max_iter, 0, self.population])
        x=list(range(0, self.time))
        plotline = plt.plot(y, label = label, color = col)
        legend_to_add = plt.legend(plotline, label, loc = loc)
        plt.gca().add_artist(legend_to_add)
        plt.scatter(x, y)
        plt.draw()
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
        # Tutaj jest caly silnik symulacji - funkcja jej odpalenia
        self.people = dict() # słownik zawierajacy wszystkich ludzi
        for i in range(self.population):
            Agent(i, self) # generujemy okreslona liczbe agentow
        self.couples_cnt = list()
        self.inf_cnt = list()
        self.known_cnt = list()
        while self.time <= self.max_iter:
            self.time += 1
            self.coupled_num = 0
            self.inf_num = 0
            self.known_num = 0
            # w kazdej iteracji zadzieja sie ponizsze funkcje: dobieranie sie w pary, zwiazki i badanie sie
            for i in self.people:
                self.people[i].coupling()
                self.people[i].relationship()
                self.people[i].testing()
            for i in self.people:
                self.coupled_num += 1 if self.people[i].partner != None else 0
                self.inf_num += 1 if self.people[i].inf == True else 0
                self.known_num += 1 if self.people[i].known == True else 0
            self.couples_cnt.append(int(self.coupled_num/2))
            self.inf_cnt.append(self.inf_num)
            self.known_cnt.append(self.known_num)
            #print('No. of couples this iteration:', int(self.coupled_num/2))
            #print('No. of infected this iteration:', self.inf_num)
            """self.plot_int(self.couples_cnt, 'Couples', 2, 'b')
            self.plot_int(self.inf_cnt, 'Infected', 9, 'g')
            self.plot_int(self.known_cnt, 'Known-Infected', 1, 'r')  """  
        self.plot(self.couples_cnt, ('Couples',), 2, 'b')
        self.plot(self.inf_cnt, ('Infected',), 9, 'g')
        self.plot(self.known_cnt, ('Known-Infected',), 1, 'r')    
        print('% of infected: {:.0%}'.format(self.inf_num/self.population))
        print('% of infected known: {:.0%}'.format(self.known_num/self.population))

#%%
soc = Society(N, MAX_ITER)
soc.run()

#turtles[0].update()