
# coding: utf-8

# # Zajęcia 5
# 
# ###[Przykład 1](http://simpy.readthedocs.org/en/latest/examples/bank_renege.html)
# Covers:
# - Resources: Resource
# - Condition events
# 
# This example models a bank counter and customers arriving at random times. Each customer has a certain patience. It waits to get to the counter until she’s at the end of her tether. If she gets to the counter, she uses it for a while before releasing it.
# New customers are created by the source process every few time steps.

# W przykładzie wystepują 2 typy agentów:
# - klienci, reprezentowani przez obiekty klasy `simpy.Process`, ktorych zachowanie opisuje funkcja `customer()`. Klienci oczekują w kolejce do stanowiska obsługi i mogą ją opuścić, kiedy czas oczekiwania na obsługę przekroczy indywidulny próg cierpliwości (`patience`)
# - stanowisko obslugi  (`counter`), reprezentowane przez obiekt klasy `simpy.Resource`
# 
# Przebieg symulacji jest sterowany przez strumień napływajacych klientów, generowany przez funkcję `source()`

# Nowym elementem wprowadzonym w symulacji jest mozliwosc opuszczenia kolejki przez oczekujacego klienta. Wykorzystujemy w tym celu wyrazenie
# ```python
# results = yield req | env.timeout(patience)
# ```
# ktore oznacza, że  agent oczekuje na zajscie __jednego z__ wymienionych zdarzen: `req` - rozpoczecie obslugi przez serwer lub `timeout(patience)` - 'wyczerpanie sie' cierpliwosci. Znak '`|`' jest operatorem alternatywy. Równoważnym sposobem zapisu powyzszego polecenia jest
# ```python
# results = yield simpy.events.AnyOf(env, (req, env.timeout(patience)))
# ```
# Istnieje rowniez mozliwosc oczekiwania na wystapienie __wszystkich__ zdarzen z uzyciem operatora koniunkcji '`&`' albo rownoważnie wywołania `simpy.events.AllOf(srodowisko, lista_zdarzen)`. Operatory koniunkcji i alternatywy można łączyć tworząc złożone wyrażenia, np.:
# ```python
# results = yield (zdarzenieA | zdarzenieB) & zdarzenieC
# ```

# In[43]:

"""
Bank renege example

Covers:

- Resources: Resource
- Condition events

Scenario:
  A counter with a random service time and customers who renege. Based on the
  program bank08.py from TheBank tutorial of SimPy 2. (KGM)

"""
import random
import simpy


RANDOM_SEED = 42
NEW_CUSTOMERS = 15  # Total number of customers
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


# In[44]:

# Setup and start the simulation
random.seed(RANDOM_SEED)
env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)
# Start processes and run
print('Bank renege')
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()

