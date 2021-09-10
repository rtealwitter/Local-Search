import numpy as np
import matplotlib.pyplot as plt

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

precomputed = {}
def msop(c, u, ordering):
    key = tuple(ordering)
    if key in precomputed: return precomputed[key]
    obj = 0
    current, previous = [], ()
    for i in range(len(ordering)):
        previous = current[:]
        current += [ordering[i]]
        obj += c(current) * (u(current) - u(previous))
    precomputed[key] = obj
    return obj

def move(ordering, i, j):
    if i == j:
        return ordering
    if i < j:
        return ordering[:i] + ordering[(i+1):(j+1)] + [ordering[i]] + ordering[(j+1):]
    if j < i:
        return ordering[:j] + [ordering[i]] + ordering[j:i] + ordering[(i+1):]

def insert(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j:]

def swap(ordering, i, j):
    return ordering[:j] + [ordering[i]] + ordering[j+1:i] + [ordering[j]] + ordering[i+1:]

def local(c, u, n, method, start=False):
    if start == False:
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
    while improved:
        improved = False
        bestordering = ordering
        for i in range(n):
            for j in range(n):
                new = method(ordering, i, j)
                objnew = msop(c, u, new)
                num_msop += 1
                if objnew < obj: 
                    obj = objnew
                    bestordering = unique(new)
                    improved = True
        ordering = bestordering
        num_rounds += 1
    return {'obj': msop(c, u, ordering), 'ordering': ordering, 'num_rounds': num_rounds, 'num_msop':num_msop}

def greedy(c, u, n):
    remaining = list(range(n))
    ordering = []
    while len(ordering) < n:
        maxitem = 'placeholder'
        maxratio = -1
        for item in remaining:
            candidate = list((*ordering,item))
            newval = (u(candidate)-u(ordering))/((c(candidate)-c(ordering)))
            if newval > maxratio:
                maxratio = newval
                maxitem = item
        ordering += [maxitem]
        remaining.remove(maxitem)
    obj = msop(c, u, ordering)
    return {'obj': obj, 'ordering': ordering}

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


