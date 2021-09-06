import toolbox
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

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

def compare(n=10, m=20, iterations=100):
    ratios = []
    for i in range(iterations):
        utility = genfacility(n,m)
        cost = modular(n)
        localdict = toolbox.local(cost, utility, n, toolbox.insert)
        #print(localdict['num_rounds']) 
        #print(localdict['num_msop']) 
        greedydict = toolbox.greedy(cost, utility, n)
        ratios += [localdict['obj']/greedydict['obj']]
        #ratios += [greedydict['obj']/localdict['obj']]
    plothist(ratios, 'Local to Greedy', title='Frequency of Local to Greedy Solution')

def profile(command):
    import cProfile
    import pstats
    cProfile.run(command, 'stats')
    p = pstats.Stats('stats')
    p.sort_stats(pstats.SortKey.TIME).print_stats(30)

def plothist(x, label, title='Frequency of Ratios', bin_num=20):
    bins = np.linspace(min(x), max(x), bin_num)
    #hist = np.histogram(x)
    #hist_dist = scipy.stats.rv_histogram(hist)
    #X = np.linspace(min(x), max(x), 100)
    #plt.plot(X, hist_dist.pdf(X), label='PDF')
    plt.hist(x, bins, alpha=0.5, label=label, color='teal')
    plt.axvline(x=1, color='red')
    plt.xlabel('Ratio')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title(title)
    plt.show()


#profile('compare()')
compare()

