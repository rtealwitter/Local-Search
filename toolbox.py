import numpy as np

def tochain(ordering):
    subset = ()
    chain = [subset]
    for item in ordering:
        subset = tuple(sorted(list(set((*subset, item)))))
        chain += [subset]
    return chain

def toordering(chain):
    ordering = []
    for i in range(1, len(chain)):
        ordering += [*set(chain[i]).difference(set(chain[i-1]))]
    return ordering

def unique(ordering):
    new = []
    for i in ordering:
        if i not in new:
            new += [i]
    return new

def msop(c, u, chain):
    obj = 0
    for i in range(len(chain)):
        current, previous = chain[i], ()
        if i > 0: previous = chain[i-1]
        obj += c(current) * (u(current) - u(previous))
    return obj

def move(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j:i] + ordering[i+1:]

def insert(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j:]

def swap(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j+1:i] + [ordering[j]] + ordering[i+1:]

def local(c, u, n, method, label='', verbose=False):
    ordering = list(range(1,n+1))
    obj = msop(c, u, tochain(ordering))
    improved = True
    while improved:
        improved = False
        bestordering = ordering
        for i in list(range(n)):
            for j in range(i):
                new = method(ordering, i, j)
                objnew = msop(c, u, tochain(new))
                if objnew < obj: 
                    obj = objnew
                    bestordering = unique(new)
                    improved = True
        ordering = bestordering
    return msop(c, u, tochain(ordering))

def greedy(c, u, n):
    remaining = list(range(1,n+1))
    ordering = []
    while len(ordering) < n:
        maxitem = 0
        maxratio = np.Inf
        for item in remaining:
            candidate = tuple(sorted((*ordering,item)))
            if u(candidate)/c(candidate) < maxratio:
                maxratio = u(candidate)/c(candidate)
                maxitem = item
        ordering += [maxitem]
        remaining.remove(maxitem)
    obj = msop(c, u, tochain(ordering))
    return obj

if __name__ == '__main__':
    pass


