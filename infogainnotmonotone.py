import numpy as np

def entropy(Sigma): 
    # Entropy of joint normal distribution with covariance matrix Sigma
    # Derivation of expression:
    # https://math.stackexchange.com/questions/2029707/entropy-of-the-multivariate-gaussian
    n = Sigma.shape[0]    
    _, logdet = np.linalg.slogdet(Sigma)
    return 1/2 * logdet + n/2 *(np.log(2*np.pi) + 1)

def infogain(Sigma, V, S):
    # Information gain described here:
    # https://en.wikipedia.org/wiki/Mutual_information#Relation_to_conditional_and_joint_entropy
    # Compute H(Sigma_V) - H(Sigma_V | Sigma_S)
    # where V and S are subsets of the universe of random variables
    Sigma_VV = Sigma[np.ix_(V,V)]
    HV = entropy(Sigma_VV) # Entropy of V

    # Build covariance matrix of random variables in V conditioned on S:
    # https://en.wikipedia.org/wiki/Multivariate_normal_distribution#Conditional_distributions
    Sigma_SS = Sigma[np.ix_(S,S)]
    Sigma_SS_inv = np.linalg.pinv(Sigma_SS)   
    Sigma_SV = Sigma[np.ix_(S,V)]
    Sigma_VS = Sigma[np.ix_(V,S)]
    Sigma_conditional = Sigma_VV - Sigma_VS @ Sigma_SS_inv @ Sigma_SV
    HVgivenS = entropy(Sigma_conditional) # Entropy of V conditioned on S

    return HV - HVgivenS

#matrix = np.random.rand(4,4)
#Sigma = matrix.T @ matrix
# Sigma is symmetric and satisfies
# the property that variance (on diagonal)
# is larger than entries
Sigma = np.matrix([[1, .1, .1],
                  [.1, 1, 1.19],
                  [.1, 1.19, 1.2]])
# V = [0,1], S = [1], T = [1,2]
infogainS = infogain(Sigma, [0], [1])
infogainT = infogain(Sigma, [0], [1,2])
print(infogainT- infogainS)
# Negative value indicates information
# gain is not monotone since I(V;S) > I(V;T)
# where T is a superset of S
