
# coding: utf-8

# ##Zad. 5.1
# Wykonaj 100 przebiegów symulacji z przykładu 1 dla populacji 100 klientów. Dla każdego przebiegu oblicz a) średni czasu obsługi(przebywania w systemie) klienta i b) ilość klientów, ktorzy zrezygnowali. Wyniki zapisza do pliku w formacie csv.

import random
import simpy
import csv


RANDOM_SEED = 42
NEW_CUSTOMERS = 100  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience
N_ITERATIONS = 100

def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)

def customer(env, name, counter, time_in_bank):
    global reneged_cnt
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
            service_time.append(wait + tib)
        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))
            service_time.append(wait)
            reneged_cnt += 1

print('Bank renege')
random.seed(RANDOM_SEED)

raczka = open('wyniki_1.csv', 'w')
pisak = csv.writer(raczka)

for i in range(1, N_ITERATIONS + 1):
    service_time = [] #lista do składowania czasu przebywania w systemie klienta
    reneged_cnt = 0 #liczba klientow rezygnujacych
    env = simpy.Environment()
    counter = simpy.Resource(env, capacity=1)
    env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
    env.run()
    pisak.writerow([round(sum(service_time)/len(service_time), 2), reneged_cnt])
    print('iteracja numer:', i)
    print('średni czasu obsługi (przebywania w systemie) klienta:', round(sum(service_time)/len(service_time), 2))
    print('LICZBA klientów, ktorzy zrezygnowali:', reneged_cnt)
    print('\n')
    
raczka.close()


# ##Zad. 5.2
# W symulacji z przykładu 1 wprowadz mozliwosc otrzymania z zalożonym prawdopodobieństwem przez klienta oczekujacego w kolejce 'pilnego telefonu', powodujacego natychmiastopwe opuszczenie kolejki lub stanowiska obsługi. Wykonaj 100 przebiegów symulacji dla populacji 100 klientów. Dla każdego przebiegu oblicz a) średni czasu obsługi(przebywania w systemie) klienta b) ilość klientów, ktorzy zrezygnowali c) ilosc klientow ktorzy otrzymali 'pilny telefon'. Wyniki zapisz do pliku w formacie csv.

import random
import simpy
import csv


RANDOM_SEED = 42
NEW_CUSTOMERS = 10  # Total number of customers
INTERVAL_CUSTOMERS = 10.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 3  # Max. customer patience
N_ITERATIONS = 10
URGENT_CALL_PARAM = 0.01


class Customer(object):
    
    def __init__(self, env, name, counter, time_in_bank):
        self.env = env
        self.name = name
        self.time_in_bank = time_in_bank
        self.client_present = True
        self.service_time = []
        self.reneged_cnt = 0
        
        self.process = env.process(self.customer_in_a_bank(counter, name, time_in_bank))
        env.process(self.urgent_call())
        
    def urgent_call(self):
        while True:
            yield self.env.timeout(random.expovariate(URGENT_CALL_PARAM))
            if self.client_present:
                self.process.interrupt()
            else:
                break
            
    def customer_in_a_bank(self, counter, name, time_in_bank):
        """Customer arrives, is served and leaves."""
        arrive = env.now
        print('%7.4f %s: Here I am' % (arrive, name))
        try:
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
                    service_time.append(wait + tib)
                else:
                    # We reneged
                    print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))
                    service_time.append(wait)
                    reneged_cnt += 1
                self.client_present = False
        except simpy.Interrupt:
            print('%7.4f %s: URGENT CALL after having been in the bank for %6.3f' % (env.now, name, env.now - arrive))
            self.client_present = False
            

print('Bank renege')
random.seed(RANDOM_SEED)

env = simpy.Environment()
counter = simpy.Resource(env, capacity=1)


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        Customer(env, 'Customer%02d' % i, counter, time_in_bank=12.0)
        yield env.timeout(random.expovariate(1.0 / interval))
        
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))

env.run()



raczka = open('wyniki_2.csv', 'w')
pisak = csv.writer(raczka)

for i in range(1, N_ITERATIONS + 1):
    service_time = [] #lista do składowania czasu przebywania w systemie klienta
    reneged_cnt = 0 #liczba klientow rezygnujacych
    env = simpy.Environment()
    counter = simpy.Resource(env, capacity=1)
    env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
    env.run()
    pisak.writerow([round(sum(service_time)/len(service_time), 2), reneged_cnt])
    print('iteracja numer:', i)
    print('średni czasu obsługi (przebywania w systemie) klienta:', round(sum(service_time)/len(service_time), 2))
    print('LICZBA klientów, ktorzy zrezygnowali:', reneged_cnt)
    print('\n')
    
raczka.close()

# ##Zad. 5.3
# W symulacji z przykładu 3 wprowadź następujące zmiany:
## dodaj kolejnego mechanika
## zastąp deterministyczne czasy naprawy losowymi z wybranego rozkładu
## w komunikatach wyjściowych zaokrąglij raportowane czasy zdarzeń do 4 miejsc dziesiętnych


import random
import simpy


RANDOM_SEED = 42
PT_MEAN = 10.0         # Avg. processing time in minutes
PT_SIGMA = 2.0         # Sigma of processing time
MTTF = 300.0           # Mean time to failure in minutes
BREAK_MEAN = 1 / MTTF  # Param. for expovariate distribution
REPAIR_TIME_PARAM = 0.1     # Time it takes to repair a machine in minutes
JOB_DURATION = 30.0    # Duration of other jobs in minutes
NUM_MACHINES = 10      # Number of machines in the machine shop
WEEKS = 4              # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes


def repairing_time():
    return random.expovariate(REPAIR_TIME_PARAM)

def time_per_part():
    """Return actual processing time for a concrete part."""
    return random.normalvariate(PT_MEAN, PT_SIGMA)

def time_to_failure():
    """Return time until next failure for a machine."""
    return random.expovariate(BREAK_MEAN)


class Machine(object):
    """A machine produces parts and my get broken every now and then.

    If it breaks, it requests a *repairman* and continues the production
    after the it is repaired.

    A machine has a *name* and a numberof *parts_made* thus far.

    """
    def __init__(self, env, name, repairman):
        self.env = env
        self.name = name
        self.parts_made = 0
        self.broken = False

        # Start "working" and "break_machine" processes for this machine.
        self.process = env.process(self.working(repairman, name))
        env.process(self.break_machine(name))

    def working(self, repairman, name):
        """Produce parts as long as the simulation runs.

        While making a part, the machine may break multiple times.
        Request a repairman when this happens.

        """
        while True:
            # Start making a new part
            done_in = time_per_part()
            while done_in:
                try:
                    # Working on the part
                    start = self.env.now
                    yield self.env.timeout(done_in)
                    done_in = 0  # Set to 0 to exit while loop.

                except simpy.Interrupt:
                    self.broken = True
                    done_in -= self.env.now - start  # How much time left?

                    # Request a repairman. This will preempt its "other_job".
                    with repairman.request(priority=1) as req:
                        print('%7.4f %s: Requesting a repairman...' % (env.now, name))
                        yield req
                        yield self.env.timeout(repairing_time())
                        print('%7.4f %s: Repairing done' % (env.now, name))

                    self.broken = False

            # Part is done.
            self.parts_made += 1

    def break_machine(self, name):
        """Break the machine every now and then."""
        while True:
            yield self.env.timeout(time_to_failure())
            if not self.broken:
                # Only break the machine if it is currently working.
                print('%7.4f %s: Machine broken!' % (env.now, name))
                self.process.interrupt()


def other_jobs(env, repairman):
    """The repairman's other (unimportant) job."""
    while True:
        # Start a new job
        done_in = JOB_DURATION
        while done_in:
            # Retry the job until it is done.
            # It's priority is lower than that of machine repairs.
            with repairman.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    done_in -= env.now - start


# Setup and start the simulation
print('Machine shop')
random.seed(RANDOM_SEED)  # This helps reproducing the results


# Create an environment and start the setup process
env = simpy.Environment()
repairman = simpy.PreemptiveResource(env, capacity=2)
machines = [Machine(env, 'Machine %d' % i, repairman)
        for i in range(NUM_MACHINES)]
env.process(other_jobs(env, repairman))

# Execute!
env.run(until=SIM_TIME)

# Analyis/results
print('Machine shop results after %s weeks' % WEEKS)
for machine in machines:
    print('%s made %d parts.' % (machine.name, machine.parts_made))

