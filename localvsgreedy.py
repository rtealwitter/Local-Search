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

def compare_ratio(n, cost_function, utility_function, iterations, num_comparisons):
    start = time.time()
    greedy_ratio, local_ratio = [], []
    for i in range(iterations):
        gc.collect()
        utility = utility_function(n)
        cost = cost_function(n)
        msop_saved = {():0}
        #optimaldict = toolbox.optimal(cost, utility, n, msop_saved=msop_saved)
        greedydict = toolbox.greedy(cost, utility, n)
        localdict_random = toolbox.repeatlocal(cost, utility, n, toolbox.move, runs=5, msop_saved=msop_saved, num_comparisons=num_comparisons)
        denominator = min(greedydict['obj'], localdict_random['obj'])
        greedy_ratio += [greedydict['obj']/denominator] 
        local_ratio += [localdict_random['obj']/denominator] 
        #localdict_greedy = toolbox.local(cost, utility, n, toolbox.move, msop_saved = msop_saved, start=greedydict['ordering'])
        #localdict_cost = toolbox.local(cost, utility, n, toolbox.move, start='cost')
    print('Time:', time.time()-start)
    return greedy_ratio, local_ratio
    
def profile(command):
    import cProfile
    import pstats
    cProfile.run(command, 'stats')
    p = pstats.Stats('stats')
    p.sort_stats(pstats.SortKey.TIME).print_stats(30)

def plothist(xs, labels, iterations, n, problem, items, bin_num=20):
    colors = ['#D12757', '#75CDFA', '#2437E6', '#FF6A10']
    bins = np.linspace(min(sum(xs, [])), max(sum(xs,[])), bin_num)
    for i in range(len(labels)):
        plt.hist(xs[i], bins, alpha=0.5, label=labels[i], color=colors[i])
    plt.axvline(x=1, color='red')
    plt.xlabel('Objective Value')
    plt.ylabel('Frequency ({} Iterations)'.format(iterations))
    plt.legend()
    plt.suptitle('Histogram of Greedy and Local Search Performance Against Best Heuristic')
    plt.title(f'{problem} with {n} {items}')
    plt.savefig(f'graphics/localvsgreedy_{problem.lower().split()[0]}.pdf')
    plt.clf()

iterations = 100
n = 40
#np.random.seed(1)
greedy_ratio, local_ratio = compare_ratio(n=n, cost_function=modular, utility_function=setcover.gencover, iterations=iterations, num_comparisons=np.inf)
plothist([greedy_ratio, local_ratio], ['Greedy', 'Local'], iterations=iterations, n=n, problem='Set Cover', items='Sets')
greedy_ratio, local_ratio = compare_ratio(n=n, cost_function=modular, utility_function=facilitylocation.genfacility, iterations=iterations, num_comparisons=np.inf)
plothist([greedy_ratio, local_ratio], ['Greedy', 'Local'], iterations=iterations, n=n, problem='Facility Location', items='Facilities')
greedy_ratio, local_ratio = compare_ratio(n=n, cost_function=modular, utility_function=entropy.genentropy, iterations=iterations, num_comparisons=np.inf)
plothist([greedy_ratio, local_ratio], ['Greedy', 'Local'], iterations=iterations, n=n, problem='Entropy', items='Sensors')
