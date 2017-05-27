"""
Implementation of basic M/M/1/K queue
"""
import simpy
import random
import statistics
import time

class mm1k_sim:
    def customer(self):    
        start = self.env.now
        if self.customer_count < self.k:
            self.customer_count += 1
            with self.bcs.request() as req:
                yield req
                yield self.env.timeout(random.expovariate(self.sr))
                self.in_system.append(self.env.now - start)
                self.customer_count -= 1

    def arrivals(self):
        while True:
            self.env.process(self.customer())
            yield self.env.timeout(random.expovariate(self.ar))

    def run(self, ar, sr, k, max_time):
        self.ar = ar
        self.sr = sr
        self.k = k # maximum customers in system
        self.customer_count = 0 # current customers in system
        self.max_time = max_time
        self.env = simpy.Environment()
        self.bcs = simpy.Resource(self.env)
        self.in_system = []
        self.env.process(self.arrivals())
        self.env.run(until=self.max_time)
        return [statistics.mean(self.in_system), theory_mm1k(ar, sr, k)]

def theory_mm1k(ar, sr, k):
    rho = ar/sr
    probs = [1/(k + 1)]*(k + 1)
    if abs(rho - 1) > 1e-8: # handle rho == 1 case
        probs[0] = (1 - rho) / (1 - rho**(k+1))
        for i in range(1, k + 1):
            probs[i] = rho**i * probs[0]
    return sum(probs[i] * i for i in range(1, k + 1)) / (ar*(1 - probs[k]))

begin = time.time()
print(mm1k_sim().run(0.9, 1, 10, 1000))
print(time.time() - begin)

