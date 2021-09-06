import toolbox
import numpy as np

def toindex(S):
    return [i-1 for i in S]

def genfacility(n, m, a=10, b=100):
    A = np.random.randint(a,b,size=(n,m))
    return lambda S : 0 if len(S) == 0 else np.sum(np.amax(A[toindex(S)], axis=0))

def modular(n, a=10, b=100):
    costs = np.random.randint(a,b,n)
    return lambda S : 0 if len(S) == 0 else np.sum(costs[toindex(S)])


n = 10
m = 40
iterations = 100
ratios = []
for i in range(iterations):
    utility = genfacility(n,m)
    cost = modular(n)
    localobj, localorder, num_rounds = toolbox.local(cost, utility, n, toolbox.insert)
    print(num_rounds) 
    greedyobj, greedyorder = toolbox.greedy(cost, utility, n)
    ratios += [greedyobj/localobj]

toolbox.plothist([ratios], ['Ratio'])


