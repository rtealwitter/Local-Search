import toolbox
import random
import numpy as np
from scipy.special import comb
import matplotlib.pyplot as plt

def move(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j:i] + ordering[i+1:]

def insert(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j:]

def swap(ordering, i, j):
    changed = ordering[:j] + [ordering[i]] + ordering[j+1:i] + [ordering[j]] + ordering[i+1:]
    return ordering[:j] + [ordering[i]] + ordering[j+1:i] + [ordering[j]] + ordering[i+1:]

def improve(fm, gm, n, method, label='', verbose=False):
    ordering = list(range(1,n+1))
    obj = toolbox.msop(fm, gm, toolbox.tochain(ordering))
    objmin, chainmin = toolbox.solvemsop(n, fm, gm)
    counter = 0
    improved = True
    while improved:
        improved = False
        for i in list(range(n))[::-1]:
            for j in range(i):
                new = method(ordering, i, j)
                objnew = toolbox.msop(fm, gm, toolbox.tochain(new))
                if objnew < obj:
                    obj = objnew
                    ordering = toolbox.unique(new)
                    improved = True
                counter += 1
    if verbose:
        print(objmin)
        print(toolbox.toordering(chainmin))
        print(ordering)
    if obj/objmin > 4:
        print('Local ratio above 4: ', obj/objmin)
        print(label)
        for a in toolbox.powerset(list(range(1,n+1))):
            print('subset, f[subset]', a, fm(a))
        for a in toolbox.powerset(list(range(1,n+1))):
            print('subset, g[subset', a, gm(a))
    return obj/objmin

def greedy(fm, gm, n):
    remaining = list(range(1,n+1))
    ordering = []
    while len(ordering) < n:
        maxitem = 0
        maxratio = np.Inf
        for item in remaining:
            candidate = tuple(sorted((*ordering,item)))
            if gm(candidate)/fm(candidate) < maxratio:
                maxitem = item
        ordering += [item]
        remaining.remove(item)
    obj = toolbox.msop(fm, gm, toolbox.tochain(ordering))
    objmin, chainmin = toolbox.solvemsop(n, fm, gm)
    if obj/objmin > 4:
        print('Greedy ratio above 4: ', obj/objmin)
        for a in toolbox.powerset(list(range(1,n+1))):
            print('subset, f[subset]', a, fm(a))
        for a in toolbox.powerset(list(range(1,n+1))):
            print('subset, g[subset', a, gm(a))
    return obj/objmin

def compareapproximation(n, iterations):
    ratios = {'Move':[], 'Insert':[],'Greedy':[]}
    for i in range(iterations):
        fm = toolbox.newsubadditive(n, a=1, b=100, subadditive=True, label="f")
        gm = toolbox.newsubadditive(n, a=1, b=10, subadditive=True, label="g")
        ratios['Move'] += [improve(fm, gm, n, move, label='Move')]
        ratios['Insert'] += [improve(fm, gm, n, insert, label='Insert')]
        ratios['Greedy'] += [greedy(fm, gm, n)]

    for label in ratios:
        plt.hist(ratios[label], bins=50, alpha=.5, edgecolor='black', label=label)
    plt.legend()
    plt.title('Approximating MSOP with n='+str(n))
    plt.ylabel('Frequency')
    plt.xlabel('Approximation Ratio')
    plt.savefig('graphics/localapproxratio.pdf')

#np.random.seed(1)
n = 6
verbose = True
#for i in range(1000):
np.random.seed(552)
cost = toolbox.newmodular(n, label='c', verbose=verbose)
utility = toolbox.newsubadditive(n, label='u', verbose=verbose)
ratio = improve(cost, utility, n, insert, verbose=verbose)
print(ratio)
    #if ratio > 1:
    #    print(i, ratio)
