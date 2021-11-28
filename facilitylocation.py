import numpy as np
from scipy.spatial.distance import cdist

def distancematrix(n,m,a,b, dim=2):
    customerpoints = np.random.uniform(a,b,size=(m,dim))
    facilitypoints = np.random.uniform(a,b,size=(n,dim))
    return np.reciprocal(cdist(facilitypoints, customerpoints))

def genfacility(n, m=100, a=0, b=1):
    # n = number of facilities
    # m = number of customers
    A = np.random.uniform(a,b,size=(n,m))
    A = distancematrix(n,m,a=a,b=b,dim=3)
    utility_saved = {():0}
    def utility(S):
        key = tuple(S)
        if key in utility_saved: return utility_saved[key]
        AS = A[list(S)]
        maxrow = np.amax(AS, axis=0)
        val = maxrow.sum()
        utility_saved[key] = val
        return val
    return utility