# <codecell>

# Zad. 3.1
# Zaproponuj zmiany w kodzie poniższej symulacji, które wygenerują histogram 
# czasu oczekiwania w kolejce.
#
# **Wskazówka:** skorzystaj z funkcji `hist()` modułu `matplotlib.pyplot`
# (przykład użycia w notatkach w sekcji wyjaśniającej zastosowanie 
# rozkładu wykładniczego)

import random as rnd
from matplotlib.pyplot import hist

N = 10000  # number of events (arrivals) to simulate
# parametr 'lambda' rozkladu wykladniczego, 
# z ktorego generujemy kolejne zdarzenia
arrival_rate = 1
arrival = 0  # first arrival at time 0
endtime = 0  # init processing end time

arrhist = []  # to store arrival history
qhist = []   # to store history of processing end times
q = []  # The Queue
quetime = []
starthist = []

for i in range(N):
    arrival += rnd.expovariate(arrival_rate)
    q.append(arrival)
    while endtime <= arrival:
        arrtime = q.pop(0)
        starttime = max(arrtime, endtime)  # processing start time
        endtime = starttime + rnd.expovariate(2)  # processing
        quetime.append(starttime - arrtime)  # store waiting history
    arrhist.append(arrival)  # store arrival history
    qhist.append(len(q))  # store the queue size history
hist(quetime)



# <codecell>

# Zad. 3.2
# W Zad 3.1 zmien typ kolejki z M/M/1 na M/M/2 
# (ze wspolna kolejka)

# <codecell>

# Zad. 3.3
# W oparciu o klasę bazową `Figura` zaproponuj implementację klasy
# potomnej `Trojkat` reprezentującej dowolny trójkąt.

class Figura:

    def __init__(self):
        raise NotImplementedError()

    def powierzchnia(self):
        '''oblicza pole powierzchni figury'''
        raise NotImplementedError("powierzchnia() must be implemented")

    def obwod(self):
        '''oblicza obwód figury'''
        raise NotImplementedError("obwod() must be implemented")

# Przykład implementacji klasy potomnej `Prostokat`
class Prostokat(Figura):
    '''klasa reprezentuje prostokąt w wymiarach dlug x szer'''

    def __init__(self, dlug, szer):
        self.dlug = dlug
        self.szer = szer
     
    def powierzchnia(self):
        '''oblicza pole powierzchni prostokąta'''
        return self.dlug * self.szer

    def obwod(self):
        '''oblicza obwód prostokąta'''
        return 2 * (self.dlug + self.szer)
        
f1 = Prostokat(10,20)
f1.obwod()

# <codecell>

# Zad. 3.4
# W oparciu o klasę bazową `Figura` zaproponuj implementację klasy
# potomnej `Elipsa` reprezentującej dowolną elipsę.


# <codecell>

# Zad. 3.5
# Zastanów się czy klasę `Koło` można zaimplementować jako klasę potomną
# klasy `Elipsa`? Jeśli tak, zaproponuj odpowiednią implementację.


# <codecell>

# Zad. 3.6
# W ponizszym kodzie zmien sposob obslugi klientow 
# z dwustanowiskowej ze wspolna kolejka 
# na dwustanowiskowa z dwoma kolejkami
# przybywajacy klient wybiera krotsza z kolejek

import simpy
import random

NEW_CUSTOMERS = 5  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, counter, time_in_bank):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_bank)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))


# Setup and start the simulation
print('Bank renege')
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()