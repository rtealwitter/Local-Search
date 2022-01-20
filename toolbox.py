import numpy as np
import matplotlib.pyplot as plt
import itertools

def unique(ordering):
    new = []
    for i in ordering:
        if i not in new:
            new += [i]
    return new

def clevermsop(c, u, ordering, previous_msop=False, msop_saved=False):
    if previous_msop == False: return msop(c, u, ordering, msop_saved) 
    

def msop(c, u, ordering, msop_saved=False):
    key = tuple(ordering)
    if isinstance(msop_saved,dict):
        if key in msop_saved: return msop_saved[key]
    obj = 0
    current, previous = [], []
    for i in range(len(ordering)):
        previous = current[:]
        current += [ordering[i]]
        obj += c(current) * (u(current) - u(previous))
    if isinstance(msop_saved, dict): msop_saved[key] = obj
    return obj

def move(ordering, i, j):
    # move ith element to jth position
    if i == j:
        return ordering
    if i < j:
        return ordering[:i] + ordering[(i+1):j] + [ordering[i]] + ordering[j:]
    if j < i:
        return ordering[:j] + [ordering[i]] + ordering[j:i] + ordering[(i+1):]

def clevermove(ordering, i, j, c, u, previous_msop=False):
    new_ordering = move(ordering, i, j)
    new_msop = []
    if previous_msop == False or j == 0:     
        current, previous = [], []
        for i in range(len(new_ordering)):
            previous = current[:]
            current += [new_ordering[i]]
            new_msop += [c(current) * (u(current)-u(previous))]
    else:
        new_msop = previous_msop[:]
        if j >= 2: new_msop[j-2] = c(new_ordering[:j-1])*(u(new_ordering[:j-1])-u(new_ordering[:j-2]))
        new_msop[j-1] = c(new_ordering[:j])*(u(new_ordering[:j])-u(new_ordering[:j-1]))
        new_msop[j] = c(new_ordering[:j+1])*(u(new_ordering[:j+1])-u(new_ordering[:j]))
    return new_msop

def insert(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j:]

def swap(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j+1:i] + [ordering[j]] + ordering[i+1:]

def local(c, u, n, start='random'):
    check = False#True
    if start == 'random':
        ordering = list(np.random.permutation(list(range(n))))
    elif start == 'cost':
        costs = [c([item]) for item in range(n)]
        ordering = list(np.argsort(costs))
    else:
        ordering = start
    obj = msop(c, u, ordering)
    improved = True
    num_rounds = 0
    num_msop = 1
    previous_msop = False
    while improved:
        improved = False
        bestordering = ordering
        for i in range(n):
            for j in range(n):
                previous_msop = clevermove(ordering, i, j, c, u, previous_msop)
                objnew = sum(previous_msop)
                if check:
                    objcheck = msop(c, u, move(ordering, i, j))
                    assert np.allclose(objcheck, objnew)
                num_msop += 1
                if objnew < obj: 
                    obj = objnew
                    bestordering = move(ordering, i, j)
                    improved = True
        ordering = bestordering
        num_rounds += 1
        if num_rounds > n:
            break
    return {'obj': msop(c, u, ordering), 'ordering': ordering, 'num_rounds': num_rounds, 'num_msop':num_msop}

def repeatlocal(c, u, n, runs):
    mindict = local(c,u,n,start='cost')
    minval = mindict['obj']
    for i in range(runs-1):
        newdict = local(c, u, n, start='random')
        if newdict['obj'] < minval:
            mindict = newdict
            minval = newdict['obj']
    return mindict

def greedy(c, u, n):
    remaining = list(range(n))
    ordering = []
    while len(ordering) < n:
        maxitem = 'placeholder'
        maxratio = - np.inf
        for item in remaining:
            candidate = ordering + [item]
            newval = (u(candidate)-u(ordering))/((c(candidate)-c(ordering)))
            if newval > maxratio:
                maxratio = newval
                maxitem = item
        ordering += [maxitem]
        remaining.remove(maxitem)
    obj = msop(c, u, ordering)
    return {'obj': obj, 'ordering': ordering}

def optimal(c, u, n, msop_saved={():0}):
    permutations = itertools.permutations(range(n))
    bestobj = np.Inf
    bestordering = []
    for perm in permutations:
        newobj = msop(c,u,perm,msop_saved=msop_saved)
        if newobj < bestobj:
            bestobj = newobj
            bestordering = perm
    return {'obj':bestobj, 'ordering':bestordering}

def plothist(xs, labels, title='Frequency of Ratios', bin_num=20):
    bins = np.linspace(min(sum(xs, [])), max(sum(xs, [])), bin_num)
    for i in range(len(labels)):
        plt.hist(xs[i], bins, alpha=0.5, label=labels[i])
    plt.xlabel('Ratio')
    plt.ylabel('Frequency')
    plt.legend()
    plt.title(title)
    plt.show()

if __name__ == '__main__':
    pass


