import toolbox
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import time

def distancematrix(n,m,a=0,b=1, dim=2):
    customerpoints = np.random.randint(a,b,size=(m,dim))
    facilitypoints = np.random.randint(a,b,size=(n,dim))

def genfacility(n, m, a=0, b=1):
    # n = number of facilities
    # m = number of customers
    A = np.random.uniform(a,b,size=(n,m))
    def utility(S):
        if len(S) == 0: return 0
        AS = A[list(S)]
        maxrow = np.amax(AS, axis=0)
        val = maxrow.sum()
        return val
    return utility

def modular(n, a=0, b=1):
    costs = np.random.uniform(a,b,n)
    def cost(S): 
        if len(S) == 0: return 0
        val = costs[list(S)].sum()
        return val
    return cost

def compare_ratio(n=20, m=20, iterations=100):
    ratios_greedy, ratios_random, ratios_cost = [], [], []
    for i in range(iterations):
        utility = genfacility(n,m)
        cost = modular(n)
        greedydict = toolbox.greedy(cost, utility, n)
        localdict_greedy = toolbox.local(cost, utility, n, toolbox.move, start=greedydict['ordering'])
        ratios_greedy += [localdict_greedy['obj']/greedydict['obj']]
        localdict_random = toolbox.repeatlocal(cost, utility, n, toolbox.move, runs=1)
        ratios_random += [localdict_random['obj']/greedydict['obj']]
        #localdict_cost = toolbox.local(cost, utility, n, toolbox.move, start='cost')
        #ratios_cost += [localdict_cost['obj']/greedydict['obj']]
    plothist([ratios_greedy, ratios_random], ['Greedy Start', 'Random Start'], iterations=iterations, n=n, m=m)

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
    plt.xlabel('Local to Greedy Ratio')
    plt.ylabel('Frequency ({} Iterations)'.format(iterations))
    plt.legend()
    plt.suptitle('Histogram of Local to Greedy Ratio')
    plt.title('Facility Location with {} Facilities and {} Customers'.format(n,m))
    plt.savefig('graphics/localvsgreedy.pdf')
    plt.clf()

def plotplot(x, y, label):
    plt.scatter(x, y, label=label)
    for deg in [2,3]:
        X = np.linspace(min(x), max(x), num=100)
        coeffs = np.polyfit(x, y, deg=deg)
        equation = '+'.join([str(coeffs[i]) + 'x^'+str(deg-i) for i in range(len(coeffs))])
        #print(equation)
        Y = np.polyval(coeffs, X)
        plt.plot(X, Y, label='Least Squares Degree '+str(deg))
    plt.xlabel('Number of Facilities')
    plt.ylabel('Time')
    plt.legend()
    plt.title('Running Time per Iteration vs Number of Facilities')
    plt.savefig('graphics/complexity_{}.pdf'.format(label.lower()))
    plt.clf()


#profile('compare_ratio()')
compare_ratio(n=10, m =10, iterations=100)
#ns = list(range(1,21))
#compare_time(ns=ns, ms=[2*i for i in ns])
