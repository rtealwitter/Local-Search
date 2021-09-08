import toolbox
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt
import time

def genfacility(n, m, a=10, b=100):
    A = np.random.randint(a,b,size=(n,m))
    precomputed = {():0}
    def utility(S):
        key = tuple(S)
        if key in precomputed:
            return precomputed[key]
        AS = A[list(S)]
        maxrow = np.amax(AS, axis=0)
        val = maxrow.sum()
        precomputed[key] = val
        return val
    return utility

def modular(n, a=10, b=100):
    costs = np.random.randint(a,b,n)
    precomputed = {():0}
    def cost(S): 
        key = tuple(S)
        if key in precomputed:
            return precomputed[key]
        val = costs[list(S)].sum()
        precomputed[key] = val
        return val
    return cost

def compare_ratio(n=10, m=20, iterations=100):
    ratios = []
    for i in range(iterations):
        utility = genfacility(n,m)
        cost = modular(n)
        #print(localdict['num_rounds']) 
        #print(localdict['num_msop']) 
        greedydict = toolbox.greedy(cost, utility, n)
        localdict = toolbox.local(cost, utility, n, toolbox.insert, start=greedydict['ordering'])
        ratios += [localdict['obj']/greedydict['obj']]
        #ratios += [greedydict['obj']/localdict['obj']]
    plothist(ratios, 'Local to Greedy', iterations=iterations, n=n, m=m)


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

def plothist(x, label, iterations, n, m, bin_num=20):
    bins = np.linspace(min(x), max(x), bin_num)
    #hist = np.histogram(x)
    #hist_dist = scipy.stats.rv_histogram(hist)
    #X = np.linspace(min(x), max(x), 100)
    #plt.plot(X, hist_dist.pdf(X), label='PDF')
    plt.hist(x, bins, alpha=0.5, label=label, color='teal')
    plt.axvline(x=1, color='red')
    plt.xlabel('Local to Greedy Ratio')
    plt.ylabel('Frequency ({} Iterations)'.format(iterations))
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
compare_ratio()
ns = list(range(1,21))
compare_time(ns=ns, ms=[2*i for i in ns])

