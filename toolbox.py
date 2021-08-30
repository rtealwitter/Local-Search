import itertools
import numpy as np
import random
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

def constraints(subset, f):
    upperbounds, lowerbounds = [], []
    for i in range(len(subset)):
        lowerbounds += [f[subset[:i] + subset[(i+1):]]]
    for S in powerset(subset):
        for T in powerset(subset):
            if unionize(S,T) == subset and S != subset and T != subset and S != () and T != ():                    
                upperbounds += [f[S] + f[T] - f[intersect(S,T)]]
    return min(upperbounds), max(lowerbounds)

def newfunction(n,a=1,b=10, subadditive=True, verbose=False, label="f"):
    universe = list(range(1,n+1))
    f = {():0}
    for subset in powerset(universe):
        if len(subset) == 1: # singleton
            f[subset] = random.uniform(a,b)
        elif len(subset) > 1:
            upperbound, lowerbound = constraints(subset, f)
            if upperbound < lowerbound: print('problem!')
            f[subset] = random.uniform(lowerbound, upperbound)
            print(lowerbound, upperbound)
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

#newsubmodular(4)

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

def getchains(current, chain):
    chains = []
    for subset in powerset(current):
        if len(subset) == 0:
            chains += [[(), current] + chain]
        elif len(subset) < len(current):
            chains += getchains(subset, [current]+chain[:])
    return chains

def msop(fm, gm, chain):
    obj = 0
    for i in range(len(chain)):
        current, previous = chain[i], ()
        if i > 0: previous = chain[i-1]
        obj += fm(current) * (gm(current) - gm(previous))
    return obj

def solvemsop(n, fm, gm):
    chains = getchains(tuple(range(1,n+1)),[])
    objectives = []
    for chain in chains:
        objectives += [msop(fm, gm, chain)]
    minimum = min(objectives)
    minimumchain = chains[objectives.index(minimum)]
    return minimum, minimumchain

def density(fd, gd, candidate, start=()):
    if candidate == () and start != (): # exclude case where candidate is empty set
        return np.Inf
    if not set(start) < set(candidate): # ensure set is subset of candidate
        return np.Inf
    if gd(candidate) == gd(start): # prevent division by 0
        return np.Inf
    return (fd(candidate)-fd(start))/(gd(candidate)-gd(start))

def solvedensity(n, fd, gd, start=()):
    objectives = [np.Inf]
    for candidate in powerset(range(1,n+1)):
        if candidate != ():
            objectives += [density(fd, gd, candidate, start)]
    minimum = min(objectives)
    minimumcandidate = powerset(range(1,n+1))[objectives.index(minimum)]
    if minimum == np.Inf:
        minimumcandidate = tuple(range(1,n+1))
    return minimum, minimumcandidate

def sml(fs, gs, lowerbound, candidate):
    if gs(candidate) < lowerbound:
        return np.Inf
    return fs(candidate)

def solvesml(n, fs, gs, lowerbound):
    objectives = []
    for candidate in powerset(range(1,n+1)):
        objectives += [sml(fs, gs, lowerbound, candidate)]
    minimum = min(objectives)
    minimumcandidate = powerset(range(1,n+1))[objectives.index(minimum)]
    return minimum, minimumcandidate

def plot(x, subtitle="", file=""):
    plt.hist(x)
    plt.suptitle("Histogram of Reduction/Optimal")
    plt.title(subtitle)
    plt.ylabel("Count")
    plt.xlabel("Reduction/Optimal")
    if file != "":
        plt.savefig(file)
    else:
        plt.show()


f = newfunction(3, verbose=True)
checkproperties(3, f, verbose=True)


