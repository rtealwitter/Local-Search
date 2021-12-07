import numpy as np
import random

def read_partial(filename, COMMON_SENSORS):
    num_common = len(COMMON_SENSORS)
    partial_observations = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            vals = line.split()
            if len(vals) >= 5: 
                sensor_id, temp = int(vals[3]), float(vals[4])
                time = vals[0] + '/' + vals[1][:5] # date and time to the minute
                # Within range of recorded temperature in Berkeley, CA
                if -4 <= temp and temp <= 42 and sensor_id in COMMON_SENSORS:
                    if time not in partial_observations:
                        partial_observations[time] = ['NA']*num_common
                    partial_observations[time][COMMON_SENSORS.index(sensor_id)] = temp                
    preprocessed = {}
    for time in partial_observations:
        if partial_observations[time].count('NA') < num_common - 1:
            preprocessed[time] = partial_observations[time]
    return preprocessed

def build_covariance_pair(partial_observations, common_sensors):
    num_sensors = len(common_sensors)
    sigma = np.zeros((num_sensors, num_sensors))
    mean = np.zeros(num_sensors)
    for i in range(num_sensors):
        total, num = 0, 0
        sensor_i = common_sensors[i]
        for time in partial_observations:
            if sensor_i >= len(partial_observations[time]):
                print(common_sensors)
                print(i)
                print(sensor_i)
                print(partial_observations[time])
            value = partial_observations[time][sensor_i]
            if  value != 'NA':
                total += value
                num += 1
        mean[i] = total/num
    for i in range(num_sensors):
        sensor_i = common_sensors[i]
        for j in range(i, num_sensors):
            sensor_j = common_sensors[j]
            total, num = 0, 0
            for time in partial_observations:
                value_i = partial_observations[time][sensor_i]
                value_j = partial_observations[time][sensor_j]
                if  value_i != 'NA' and value_j != 'NA':
                    total += (value_i - mean[i])*(value_j - mean[j])
                    num += 1
            sigma[i,j] = sigma[j,i] = total/num
    return sigma

def convert_observations(partial_observations):
    print(len(partial_observations))
    observations = []
    for time in partial_observations:
        if partial_observations[time].count('NA') == 0:
            observations += [partial_observations[time]]

    return np.array(observations).T # (num_sensors, num_observations)

def build_covariance_vector(observations):
    xbar = np.mean(observations, 1) # (num_sensors,)
    num_sensors, num_observations = observations.shape
    sigma = np.zeros((num_sensors,num_sensors))
    for i in range(num_observations):
        xi = observations[:,i] # (num_sensors,)
        outer = np.outer(xi-xbar, xi-xbar)/num_observations
        sigma = np.add(outer, sigma) 
    return sigma

def H(covariance_matrix): 
    n = covariance_matrix.shape[0]
    # https://math.stackexchange.com/questions/2029707/entropy-of-the-multivariate-gaussian
    sign, logdet = np.linalg.slogdet(covariance_matrix)
    det = np.exp(logdet)
    return n/2 * np.log(2*np.pi) + np.log(det)/2 + n/2

def build_conditional(S, sigma, variance_scalar=1):
    V = list(range(sigma.shape[0]))
    sigma_SS = sigma[np.ix_(S,S)]
    sigma_SV = sigma[np.ix_(S,V)]
    sigma_VS = sigma[np.ix_(V,S)]
    sigma_VV = sigma[np.ix_(V,V)]
    sigma_SS_inv = np.linalg.inv(sigma_SS + np.eye(len(S))*variance_scalar)
    return sigma_VV - sigma_VS @ sigma_SS_inv @ sigma_SV
filename = 'data/temperature.txt'
# Sensors with more than 10,000 observations with temps within recorded temps of Berkeley, CA
COMMON_SENSORS = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54]
partial_observations = read_partial(filename, COMMON_SENSORS)
def genentropy(n): 
    common_sensors = random.sample(list(range(len(COMMON_SENSORS))), n)
    sigma = build_covariance_pair(partial_observations, common_sensors)
    #observations = convert_observations(partial_observations)
    #sigma2 = build_covariance_vector(observations)
    utility_saved = {():0}
    HV = H(sigma)
    def utility(S):
        key = tuple(S)
        if key in utility_saved: return utility_saved[key]
        conditional = build_conditional(S, sigma)
        HVS = H(conditional)
        val = HV - HVS
        utility_saved[key] = val
        return val
    return utility