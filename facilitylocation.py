import numpy as np
from scipy.spatial.distance import cdist
import os

def normalize(data):
    # columns are features
    # rows are observations
    centered = data - data.min(axis=0)
    normalized = centered/centered.max(axis=0)
    return normalized

def read_citibike(filename='data/citibike.csv'):
    station_file = 'data/citibike_stations.txt'
    if not os.path.exists(station_file):
        locations = []
        with open(filename, 'r') as f:
            f.readline() # top row is names
            for raw_line in f:
                line = raw_line.split(',')
                row = [eval(line[-5]), eval(line[-4])]
                if row not in locations:
                    locations += [row]
        with open(station_file, 'w') as f:
            f.write(str(locations))
    with open(station_file, 'r') as f:
        locations = eval(f.readline())
    locations = np.array(locations)
    np.random.shuffle(locations)
    return normalize(locations)

def distance_citibike(n, m):
    stations = read_citibike()[:n,]
    people = np.random.uniform(stations.min(axis=0), stations.max(axis=0), size=(m,2))
    distances = cdist(stations, people)
    return np.reciprocal(distances)

def distancematrix(n,m,a,b, dim=2):
    customerpoints = np.random.uniform(a,b,size=(m,dim))
    facilitypoints = np.random.uniform(a,b,size=(n,dim))
    return np.reciprocal(cdist(facilitypoints, customerpoints))

def genfacility(n, m=20, a=0, b=1):
    # n = number of facilities
    # m = number of customers
    #A = np.random.uniform(a,b,size=(n,m))
    #A = distancematrix(n,m,a=a,b=b,dim=3)
    A = distance_citibike(n,m)
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
