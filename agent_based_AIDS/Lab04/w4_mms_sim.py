"""
M/M/c system with separate queues and different queue choosing policies
"""
import simpy
import random
import multiprocessing

class Queue:
    def __init__(self, ar, sr, capacity, size):
        self.ar = ar
        self.sr = sr
        self.capacity = capacity
        self.size = size # number of considered queues

    """Choose best of random self.size queues"""
    def policy(self):
        min_bcs = float('inf') # holds shortest queue length
        for i in random.sample(range(self.capacity), self.size):
            cur = self.bcs[i].count+len(self.bcs[i].queue)
            if cur < min_bcs:
                best_bcs = self.bcs[i]
                min_bcs = cur
        return best_bcs    

    def customer(self):
        start = self.env.now
        best_bcs = self.policy()
        with best_bcs.request() as req:
            yield req
            yield self.env.timeout(random.expovariate(self.sr))
            self.in_system.append(self.env.now - start)

    def arrivals(self):
        while True:
            self.env.process(self.customer())
            yield self.env.timeout(random.expovariate(self.ar))

    def run(self):
        self.env = simpy.Environment()
        self.bcs = [simpy.Resource(self.env) for i in range(self.capacity)]
        self.in_system = []
        self.env.process(self.arrivals())
        self.env.run(until=5000)
        return sum(self.in_system)/len(self.in_system)

def worker(i):
    print("{}\t{}".format(i, Queue(9, 1, 10, i).run()))

if __name__ == '__main__':
    proc_list = []
    for i in range(1,11):
        p = multiprocessing.Process(target=worker, args=(i,))
        proc_list.append(p)
        p.start()
    print(proc_list)
    for p in proc_list:
        p.join()
        print(p)
    print(proc_list)
    input("Done!")
    
