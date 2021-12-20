import numpy as np

def buildcoverinstance(n,m,target,agree,p):
    cols = []
    group_sizes = [n//target]*target + [n % target]
    for group_size in group_sizes:
        baseline = np.random.choice([0,1], size=(m,1), replace=True, p=[1-p, p])
        for _ in range(group_size):
            sameness = np.random.choice([0,1], size=(m,1), replace=True, p=[1-agree, agree])
            random = np.random.choice([0,1], size=(m,1), replace=True, p=[1-p, p])
            new = baseline*sameness + (1-sameness)*random
            cols += [new]
    return np.column_stack(cols)

def gencover(n, agree=.7, p=.3, target=4):
    m = n*2
    # n = number of sets
    # m = number of ground elements
    # target = size of conditional groups
    # agree = determines correlation within group
    # p = probability of 1
    A = buildcoverinstance(n,m,target,agree,p)
    utility_saved = {():0}
    def utility(S):
        key = tuple(S)
        if key in utility_saved: return utility_saved[key]
        AS = A[:,list(S)]
        val = sum(AS.sum(axis=1)>0)
        utility_saved[key] = val
        return val
    return utility

