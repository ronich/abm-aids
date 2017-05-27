
# coding: utf-8

# # Zajęcia 5
# 
# ###[Przykład 3](http://simpy.readthedocs.org/en/latest/examples/machine_shop.html)
# Covers:
# - Interrupts
# - Resources: PreemptiveResource
# 
# This example comprises a workshop with n identical machines. A stream of jobs (enough to keep the machines busy) arrives. Each machine breaks down periodically. Repairs are carried out by one repairman. The repairman has other, less important tasks to perform, too. Broken machines preempt theses tasks. The repairman continues them when he is done with the machine repair. The workshop works continuously.
# 
# A machine has two processes: working implements the actual behaviour of the machine (producing parts). break_machine periodically interrupts the working process to simulate the machine failure.
# 
# The repairman’s other job is also a process (implemented by other_job). The repairman itself is a PreemptiveResource with a capacity of 1. The machine repairing has a priority of 1, while the other job has a priority of 2 (the smaller the number, the higher the priority).

# Nowym elementem wprowadzonym w symulacji jest agent `mechanik` (`repairman`) reprezentowany przez obiekt klasy `simpy.PreemptiveResource`. Obiekt tej klasy reprezentuje kolejke z priorytetami zgłoszeń z mozliwoscia wywłaszczenia zgłoszeń o niższym priorytecie przez naplywajace zgłoszenia o wyższym priorytecie. W naszym przypadku wyzszy priorytet jest przypisany zgłoszeniom awarii maszyn, co powoduje że inne prace oczekujące na wykonanie przez mechanika (generowane w funkcji `other_jobs()`) sa 'wywłaszczane', nawet jesli sa juz w trakcie realizacji. Zdarzenie wywłaszczenia jest generowane jako wyjatek klasy `simpy.Interrupt`, zatem zachowanie agenta `mechanik` w przypadku wywlaszczenia jest okreslone przez kod w klauzuli `except` funkcji `other_jobs()`.

# In[5]:

"""
Machine shop example

Covers:

- Interrupts
- Resources: PreemptiveResource

Scenario:
  A workshop has *n* identical machines. A stream of jobs (enough to
  keep the machines busy) arrives. Each machine breaks down
  periodically. Repairs are carried out by one repairman. The repairman
  has other, less important tasks to perform, too. Broken machines
  preempt theses tasks. The repairman continues them when he is done
  with the machine repair. The workshop works continuously.

"""
import random
import simpy


RANDOM_SEED = 42
PT_MEAN = 10.0         # Avg. processing time in minutes
PT_SIGMA = 2.0         # Sigma of processing time
MTTF = 30.0           # Mean time to failure in minutes
BREAK_MEAN = 1 / MTTF  # Param. for expovariate distribution
REPAIR_TIME = 10.0     # Time it takes to repair a machine in minutes
JOB_DURATION = 30.0    # Duration of other jobs in minutes
NUM_MACHINES = 3       # Number of machines in the machine shop
DAYS = 3           # Simulation time in weeks
SIM_TIME = DAYS * 24 * 60/100  # Simulation time in minutes


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
    def __init__(self, env, name, repairman1, repairman2):
        self.env = env
        self.name = name
        self.parts_made = 0
        self.broken = False

        # Start "working" and "break_machine" processes for this machine.
        self.process = env.process(self.working(repairman1, repairman2))
        env.process(self.break_machine())

    def working(self, repairman1, repairman2):
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
                    print(self.name, "start working on a new part at", start)
                    yield self.env.timeout(done_in)
                    done_in = 0  # Set to 0 to exit while loop.

                except simpy.Interrupt:
                    # oops, broken down!
                    self.broken = True
                    done_in -= self.env.now - start  # How much time left?
                    print(self.name, "oops! broken down at", self.env.now, "- waiting for a repairman")

                    # Request a repairman. This will preempt its "other_job".
                    print(len(repairman1.queue))
                    with repairman1.request(priority=1) if len(repairman1.queue) <= len(repairman2.queue) else repairman2.request(priority=1) as req:
                        yield req
                        yield self.env.timeout(REPAIR_TIME)

                    print(self.name, "repaired at", self.env.now)
                    self.broken = False

            # Part is done.
            self.parts_made += 1

    def break_machine(self):
        """Break the machine every now and then."""
        while True:
            yield self.env.timeout(time_to_failure())
            if not self.broken:
                # Only break the machine if it is currently working.
                self.process.interrupt()


def r1_other_jobs(env, repairman1):
    """The repairman 1's other (unimportant) job."""
    while True:
        # Start a new job
        done_in = JOB_DURATION
        print("Repairman 1 starting yet another less important job at", env.now)
        while done_in:
            # Retry the job until it is done.
            # It's priority is lower than that of machine repairs.
            with repairman1.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    print("Repairman 1 called to repair a machine at", env.now)                    
                    done_in -= env.now - start
                    
def r2_other_jobs(env, repairman2):
    """The repairman 1's other (unimportant) job."""
    while True:
        # Start a new job
        done_in = JOB_DURATION
        print("Repairman 2 starting yet another less important job at", env.now)
        while done_in:
            # Retry the job until it is done.
            # It's priority is lower than that of machine repairs.
            with repairman2.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    print("Repairman 2 called to repair a machine at", env.now)                    
                    done_in -= env.now - start

# Setup and start the simulation
print('Machine shop')
random.seed(RANDOM_SEED)  # This helps reproducing the results


# In[6]:

# Create an environment and start the setup process
env = simpy.Environment()
repairman1 = simpy.PreemptiveResource(env, capacity=1)
repairman2 = simpy.PreemptiveResource(env, capacity=1)
machines = [Machine(env, 'Machine %d' % i, repairman1, repairman2)
        for i in range(NUM_MACHINES)]
env.process(r1_other_jobs(env, repairman1))
env.process(r2_other_jobs(env, repairman2))


# In[7]:

# Execute!
env.run(until=SIM_TIME)


# In[4]:

# Analyis/results
print('Machine shop results after %s days' % DAYS)
for machine in machines:
    print('%s made %d parts.' % (machine.name, machine.parts_made))

