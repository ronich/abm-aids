"""
Implementation of basic M/M/c queue
"""
import simpy
import random

def customer(cid):
    if REPORT:
        print('Arrived {} at {}'.format(cid, env.now))
    start = env.now
    with bcs.request() as req:
        yield req
        if REPORT:
            print('Start {} service at {}'.format(cid, env.now))
        yield env.timeout(random.expovariate(SR))
        if REPORT:
            print('End {} service at {}'.format(cid, env.now))
        in_system.append(env.now - start)
        yield env.timeout(1)

def arrivals():
    cid = 1
    while True:
        env.process(customer(cid))
        yield env.timeout(random.expovariate(AR))
        cid += 1

CAPACITY = 1    # server capacity
REPORT = True   # do we need diagnostic messages?
AR = 1.5        # arrival rate
SR = 1          # service rate

env = simpy.Environment()
bcs = simpy.Resource(env, capacity=CAPACITY)
in_system = []
env.process(arrivals())
env.run(until=5)
print(sum(in_system)/len(in_system))
# should be 1/(SR*(1-AR/SR)) for M/M/1
# should be 1/(SR*(1-(AR/SR)^2/4)) for M/M/2

