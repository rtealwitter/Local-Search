import toolbox
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import time

def distancematrix(n,m,a,b, dim=2):
    customerpoints = np.random.uniform(a,b,size=(m,dim))
    facilitypoints = np.random.uniform(a,b,size=(n,dim))
    return np.reciprocal(cdist(facilitypoints, customerpoints))

def genfacility(n, m, a=0, b=1):
    # n = number of facilities
    # m = number of customers
    A = np.random.uniform(a,b,size=(n,m))
    A = distancematrix(n,m,a=a,b=b,dim=3)
    utility_saved = {():0}
    def utility(S):
        key = tuple(S)
        if key in utility_saved: return utility_saved[key]
        AS = A[list(S)]
        maxrow = np.amax(AS, axis=0)
        val = maxrow.sum()
        utility_saved[key] = val
        return val
    return utility

def modular(n, a=0, b=1):
    costs = np.random.uniform(a,b,n)
    cost_saved = {():0}
    def cost(S): 
        key = tuple(S)
        if key in cost_saved: return cost_saved[key]
        val = costs[list(S)].sum()
        cost_saved[key] = val
        return val
    return cost

def compare_ratio(n, m, iterations):
    start = time.time()
    greedy_ratio, local_ratio = [], []
    for i in range(iterations):
        utility = genfacility(n,m)
        cost = modular(n)
        msop_saved = {():0}
        optimaldict = toolbox.optimal(cost, utility, n, msop_saved=msop_saved)
        greedydict = toolbox.greedy(cost, utility, n)
        denominator = optimaldict['obj']
        greedy_ratio += [greedydict['obj']/denominator]
        localdict_random = toolbox.repeatlocal(cost, utility, n, toolbox.move, runs=5, msop_saved=msop_saved)
        local_ratio += [localdict_random['obj']/denominator] 
        #localdict_greedy = toolbox.local(cost, utility, n, toolbox.move, msop_saved = msop_saved, start=greedydict['ordering'])
        #localdict_cost = toolbox.local(cost, utility, n, toolbox.move, start='cost')
    plothist([greedy_ratio, local_ratio], ['Greedy', 'Local'], iterations=iterations, n=n, m=m)
    print('Time:', time.time()-start)

def compare_time(ns, ms, iterations=10):
    local_times, greedy_times = [], []
    for j in range(len(ns)):
        n, m = ns[j], ms[j]
        greedy_time, local_time = 0, 0
        for i in range(iterations):
            utility = genfacility(n,m)
            cost = modular(n)
            start = time.time()
            greedydict = toolbox.greedy(cost, utility, n)
            greedy_time += time.time() - start
            start = time.time()
            localdict = toolbox.local(cost, utility, n, toolbox.insert, start=greedydict['ordering'])
            local_time += time.time() - start
        local_times += [local_time/iterations]
        greedy_times += [greedy_time/iterations]
    plotplot(ns, greedy_times, 'Greedy')
    plotplot(ns, local_times, 'Local')


def profile(command):
    import cProfile
    import pstats
    cProfile.run(command, 'stats')
    p = pstats.Stats('stats')
    p.sort_stats(pstats.SortKey.TIME).print_stats(30)

def plothist(xs, labels, iterations, n, m, bin_num=20):
    colors = ['#D12757', '#75CDFA', '#2437E6', '#FF6A10']
    bins = np.linspace(min(sum(xs, [])), max(sum(xs,[])), bin_num)
    for i in range(len(labels)):
        plt.hist(xs[i], bins, alpha=0.5, label=labels[i], color=colors[i])
    plt.axvline(x=1, color='red')
    plt.xlabel('Ratio of Solution to Optimal')
    plt.ylabel('Frequency ({} Iterations)'.format(iterations))
    plt.legend()
    plt.suptitle('Accuracy of Greedy and Local Search by Frequency')
    plt.title('Facility Location with {} Facilities and {} Customers'.format(n,m))
    plt.savefig('graphics/localvsgreedy.pdf')
    plt.clf()

def plotplot(x, y, label):
    plt.scatter(x, y, label=label)
    for deg in [2,3]:
        X = np.linspace(min(x), max(x), num=100)
        coeffs = np.polyfit(x, y, deg=deg)
        equation = '+'.join([str(coeffs[i]) + 'x^'+str(deg-i) for i in range(len(coeffs))])
        Y = np.polyval(coeffs, X)
        plt.plot(X, Y, label='Least Squares Degree '+str(deg))
    plt.xlabel('Number of Facilities')
    plt.ylabel('Time')
    plt.legend()
    plt.title('Running Time per Iteration vs Number of Facilities')
    plt.savefig('graphics/complexity_{}.pdf'.format(label.lower()))
    plt.clf()


#profile('compare_ratio()')
np.random.seed(1)
compare_ratio(n=7, m=7, iterations=100)
#ns = list(range(1,21))
#compare_time(ns=ns, ms=[2*i for i in ns])
