from email import iterators
import toolbox
import numpy as np
import matplotlib.pyplot as plt
import time
import setcover
import facilitylocation
import entropy
import gc

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

def compare_ratio(n, cost_function, utility_function, iterations):
    greedy_ratio, local_ratio = [], []
    greedy_time, local_time = 0, 0
    for i in range(iterations):
        gc.collect()
        utility = utility_function(n)
        cost = cost_function(n)

        start = time.time()
        greedydict = toolbox.greedy(cost, utility, n)
        greedy_time += time.time() - start

        start = time.time()
        localdict_random = toolbox.repeatlocal(cost, utility, n, runs=5)
        local_time += time.time() - start

        denominator = min(greedydict['obj'], localdict_random['obj'])
        greedy_ratio += [greedydict['obj']/denominator] 
        local_ratio += [localdict_random['obj']/denominator] 
    print('Greedy Time:', greedy_time)
    print('Local Time:', local_time)
    return greedy_ratio, local_ratio
    
def profile(command):
    import cProfile
    import pstats
    cProfile.run(command, 'stats')
    p = pstats.Stats('stats')
    p.sort_stats(pstats.SortKey.TIME).print_stats(30)

def plothist(xs, labels, iterations, n, problem, items, bin_num=20):
    plt.rcParams.update({'font.size': 15})
    colors = ['#D12757', '#75CDFA', '#2437E6', '#FF6A10']
    bins = np.linspace(min(sum(xs, [])), max(sum(xs,[])), bin_num)
    for i in range(len(labels)):
        plt.hist(xs[i], bins, alpha=0.5, label=labels[i], color=colors[i])
    plt.axvline(x=1, color='red')
    plt.xlabel('Relative Objective Value')
    plt.ylabel('Frequency ({} Iterations)'.format(iterations))
    plt.legend()
    #plt.suptitle('Histogram of Greedy and Local Search Performance Against Best Heuristic')
    plt.title(f'{problem} with {n} {items}')
    plt.savefig(f'graphics/localvsgreedy_{problem.lower().split()[0]}.pdf')
    plt.clf()

iterations = 100
n = 30
np.random.seed(1)

greedy_ratio, local_ratio = compare_ratio(n=n, cost_function=modular, utility_function=setcover.gencover, iterations=iterations)
plothist([greedy_ratio, local_ratio], ['Greedy', 'Local'], iterations=iterations, n=n, problem='Pipelined Set Cover', items='Sets')
#greedy_ratio, local_ratio = compare_ratio(n=n, cost_function=modular, utility_function=facilitylocation.genfacility, iterations=iterations)
#plothist([greedy_ratio, local_ratio], ['Greedy', 'Local'], iterations=iterations, n=n, problem='Facility Location', items='Facilities')
#greedy_ratio, local_ratio = compare_ratio(n=n, cost_function=modular, utility_function=entropy.genentropy, iterations=iterations)
#plothist([greedy_ratio, local_ratio], ['Greedy', 'Local'], iterations=iterations, n=n, problem='Sensor Placement', items='Sensors')