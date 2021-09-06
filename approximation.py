import toolbox
import numpy as np
import itertools
import matplotlib.pyplot as plt

# adapted from https://docs.python.org/3/library/itertools.html#itertools-recipes
def powerset(iterable):
    "powerset([1,2,3]) --> (,) (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return [i for i in itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))]

def intersect(S, T):
    return tuple(sorted(list(set(S).intersection(set(T)))))

def unionize(S, T):
    return tuple(sorted(list(set(S + T))))

def getchains(current, chain):
    chains = []
    for subset in powerset(current):
        if len(subset) == 0:
            chains += [[(), current] + chain]
        elif len(subset) < len(current):
            chains += getchains(subset, [current]+chain[:])
    return chains

def chainwrapper(current, chain):
    chains = getchains(current, chain)
    return [chain for chain in chains if len(chain)==len(current)+1]

def constraints(subset, f):
    upperbounds, lowerbounds = [], []
    for i in range(len(subset)):
        lowerbounds += [f[subset[:i] + subset[(i+1):]]]
    for S in powerset(subset):
        for T in powerset(subset):
            if unionize(S,T) == subset and S != subset and T != subset and S != () and T != ():                    
                upperbounds += [f[S] + f[T]]
    return min(upperbounds), max(lowerbounds)

def newmodular(n, a=1, b=10, verbose=False, label="f"):
    universe = list(range(1,n+1))
    values = [a]*n #np.random.randint(a,b,n)
    f = {():0}
    for subset in powerset(universe):
        total = 0
        for item in subset:
            total += values[item-1]
        f[subset] = total
        if verbose: print("subset, {}[subset]".format(label), subset, f[subset])
    def function(a): return f[a]
    return function

def newsubadditive(n,a=1,b=3, verbose=False, label="f"):
    universe = list(range(1,n+1))
    f = {():0}
    for subset in powerset(universe):
        if len(subset) == 1: # singleton
            f[subset] = np.random.uniform(a,b)
        elif len(subset) > 1:
            upperbound, lowerbound = constraints(subset, f)
            if upperbound < lowerbound: print('problem!')
            f[subset] = np.random.uniform(lowerbound, upperbound)
        if verbose: print("subset, {}[subset]".format(label), subset, f[subset])
    def function(a): return f[a]
    return function

def newsubmodular(n,a=1,b=10):
    record = np.full((2**n,n+1), np.Inf)
    for i in range(n): record[i+1,0] = record[i+1,i+1] = np.random.uniform(a,b)
    powersets = powerset(list(range(1,n+1)))
    lastswitch = 0
    for i in range(n+1,2**n):
        if len(powersets[i]) > len(powersets[i-1]): lastswitch=i-1
        subset=powersets[i]
        print(subset,i,lastswitch)
        #print(bin(i)[2:].zfill(n))
    print(record)

def checkproperties(n, f, verbose=False):
    properties = {"monotone":True, "subadditive":True, "submodular":True}
    universe = list(range(1,n+1))
    for S in powerset(universe):
        for T in powerset(universe):            
            if set(T).issubset(set(S)) and f(T) > f(S): # monotone
                if verbose:
                    print("Not monotone:")
                    print("T, S", T, S)
                    print("f[T], f[S]", f(T), f(S))
                properties["monotone"] = False
            if f(T) + f(S) < f(unionize(S,T)): # subadditive
                if verbose:
                    print("Not subadditive:")
                    print("T, S, union", T, S, unionize(S,T))
                    print("f[T], f[S], f[union]", f(T), f(S), f(unionize(S,T)))
                properties["subadditive"] = False
            if f(T) + f(S) < f(unionize(S,T)) + f(intersect(S,T)): # submodular
                if verbose:
                    print("Not submodular:")
                    print("T, S, union, intersect(S,T)", T, S, unionize(S,T), intersect(S,T))
                    print("f[T], f[S], f[union], f[intersect(S,T)]", f(T), f(S), f(unionize(S,T)), f(intersect(S,T)))
                properties["submodular"] = False
    return properties

def solvemsop(n, c, u):
    chains = chainwrapper(tuple(range(1,n+1)),[])
    objectives = []
    for chain in chains:
        objectives += [toolbox.msop(c, u, chain)]
    minimum = min(objectives)
    minimumchain = chains[objectives.index(minimum)]
    return minimum, minimumchain

if __name__ == '__main__':
    n = 5
    verbose = False
    iterations = 1000
    localratios, greedyratios = [], []
    for i in range(iterations):
        cost = newmodular(n, a=10, b=100, label='c', verbose=verbose)
        utility = newsubadditive(n, a=10, b=100, label='u', verbose=verbose)
        minobj, minchain = solvemsop(n, cost, utility)
        localobj, localorder = toolbox.local(cost, utility, n, toolbox.insert, verbose=verbose)
        greedyobj, greedyorder = toolbox.greedy(cost, utility, n)
        localratios += [localobj/minobj]
        greedyratios += [greedyobj/minobj]
    plothist([localratios, greedyratios], ['Local', 'Greedy'])
    
    
