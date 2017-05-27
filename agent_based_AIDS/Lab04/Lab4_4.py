
# coding: utf-8

# # Zajęcia 4 cz.4

# ## SimPy - biblioteka dla DES
# Biblioteka `simpy` dostarcza gotowe klasy obiektów do budowy symulacji:
# - **procesy** (Process) - reprezentują procesy zachodzące w czasie (czynności wykonywane przez agentów)
# - **zdarzenia** (Event) - reprezentują szczególny 'punktowy' w czasie rodzaj procesu
# - **zasoby** (Resource) - reprezentują zasoby o ograniczonej pojemności, współdzielone przez procesy
# - **środowisko** (Environment), które zarządzą upływem czasu oraz koordynuje procesy, zdarzenia i dostęp do zasobów

# ###instalacja pakietu `simpy`
# Pakiet `simpy` nie jest czescia dysrubucji Anaconda. Aby go zainstalowac z poziomu wiersza poleceń systemu operacyjnego wykonujemy komende:
# 
# `pip install simpy`
# 
# albo `pip install --user simpy` jesli nie mamy uprawnień do katalogu, w którym zainstalowany jest Python.

# In[ ]:

import simpy


# Przygotowanie symulacji zaczynamy od utworzenia środowiska, w którym bedzię się ona odbywać:

# In[ ]:

env = simpy.Environment() # utworz srodowisko symulacji


# In[ ]:

type(env)


# In[ ]:

env


# Funkcja `car` definiuje protego agenta, który ma dwa stany - jazdę (`driving`) albo parkowanie (`parking`) i przełącza się między nimi w deterministyczny sposób.

# In[ ]:

def car(env):
    trip_duration = 3
    parking_duration = 5
    while True:
        print('Start parking at %d' % env.now)
        yield env.timeout(parking_duration)
        print('Start driving at %d' % env.now)
        yield env.timeout(trip_duration)


# dodajemy agenta do srodowiska symulacji

# In[ ]:

env.process(car(env))


# uruchamiamy sumulacje:

# In[ ]:

env.run(until=25)


# zegar środowiska symulacji przesunął sie o 25 jednostek, możemy kontunuować jej wykonanie:

# In[ ]:

env.run(until=40)


# wprowadzmy element losowosci:

# In[ ]:

import random as rnd
LAMBDA = 1

def car(env):
    while True:
        print('Start parking at %f' % env.now)
        yield env.timeout(rnd.expovariate(LAMBDA))
        print('Start driving at %f' % env.now)
        yield env.timeout(rnd.expovariate(LAMBDA))


# In[ ]:

env = simpy.Environment() # utworz srodowisko symulacji


# In[ ]:

env.process(car(env))


# In[ ]:

env.run(20)


# Urozmaicimy symulację przez heterogenizację populacji samochodów. Wprowadzimy też nowy typ agenta - stację paliwową.

# In[ ]:

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2) # stacja paliwowa z dwoma dystrybutorami


# In[ ]:

def car(env, name, bcs, driving_time, charge_duration):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)

    # Request one of its charging spots
    print('%s arriving at %d' % (name, env.now))
    with bcs.request() as req:
        yield req

        # Charge the battery
        print('%s starting to charge at %s' % (name, env.now))
        yield env.timeout(charge_duration)
        print('%s leaving the bcs at %s' % (name, env.now))


# In[ ]:

N = 10
for i in range(N):
    c = car(env, 'Car %d' % i, bcs, i*2, 5)
    env.process(c)


# In[ ]:

env.run()


# In[ ]:

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2)


# wydzielamy proces tankowania/ładowania do osobnej funkcji:

# In[ ]:

def charge(env, name, duration):
    # Charge the battery
    print('%s starting to charge at %s' % (name, env.now))
    yield env.timeout(duration)
    print('%s finished charging at %s' % (name, env.now))


# In[ ]:

def car(env, name, bcs, driving_time, charge_duration):
    # Simulate driving to the BCS
    yield env.timeout(driving_time)

    # Request one of its charging spots
    print('%s arriving at %d' % (name, env.now))
    with bcs.request() as req:
        yield req

        # We yield the process that process() returns
        # to wait for it to finish
        yield env.process(charge(env, name, charge_duration))
        print('%s leaving the bcs at %s' % (name, env.now))


# In[ ]:

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=2) # stacja paliwowa z dwoma dystrybutorami


# In[ ]:

N = 10
for i in range(N):
    c = car(env, 'Car %d' % i, bcs, i*2, 5)
    env.process(c)
env.run()


# encapsulate! :)

# In[ ]:

def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()
    yield env.timeout(6)
    car.action.interrupt()

class Car(object):
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        trip_duration = 2
        charge_duration = 5
        while True:
            print('Start parking and charging at %d' % self.env.now)
            # We may get interrupted while charging the battery
            try:
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                # When we received an interrupt, we stop charing and
                # switch to the "driving" state
                print('Was interrupted. Hope, the battery is full enough ')

            print('Start driving at %d' % self.env.now)
            yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)


env = simpy.Environment()
car = Car(env)
env.process(driver(env, car))
env.run(until=20)

