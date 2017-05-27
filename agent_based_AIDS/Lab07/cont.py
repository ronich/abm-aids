import random
import sys
from scipy.stats import kurtosis
import csv


def cont(n, l, s, d, time, burnin):
    def phi(theta):
        if epsilon > theta:
            return 1
        if epsilon < -theta:
            return -1
        return 0

    theta = list(map(lambda x: random.random() / l, range(n)))
    report = []

    for period in range(time):
        epsilon = random.normalvariate(0, d)
        r = sum(map(phi, theta)) / (n * l)
        if period > burnin:
            report.append(r)
        r = abs(r)
        for i in range(n):
            if random.random() < s:
                theta[i] = r
    return kurtosis(report)


def run(points, reps, seed):
    print("point,rep,l,s,d,k")
    random.seed(seed)
    with open('results.csv', 'w', newline='') as csvfile:
        resultswriter = csv.writer(csvfile)
        resultswriter.writerow("point,rep,l,s,d,k")
        for point in range(points):
            l = random.uniform(5, 20)
            s = random.uniform(0.01, 0.1)
            d = random.uniform(0.001, 0.01)
            for rep in range(reps):
                k = cont(1000, l, s, d, 1100, 100)
                values = [point, rep, l, s, d, k]
                print(values)

if __name__ == '__main__':
    try:
        points = int(sys.argv[1])
    except (ValueError, IndexError):
        points = 100
    try:
        reps = int(sys.argv[2])
    except (ValueError, IndexError):
        reps = 6
    try:
        seed = int(sys.argv[3])
    except IndexError:
        seed = None
    run(points, reps, seed)
