# A Local Search Algorithm for Min-Sum Submodular Cover

### Introduction
This repository holds the code and dataset we used to run
experiments.
We use the following files:

* `toolbox.py` contains the code for calculating the objective value of Min-Sum Submodular Cover in addition to the local search and greedy algorithms.

* `data/` contains the coordinates of CitiBike stations and the cleaned temperature sensor observations used to build the corresponding utility functions.

* `setcover.py` contains the code for generating random Pipelined Set Cover instances from the method described in Babu et al. (2004).

* `facilitylocation.py` contains the code for choosing random CitiBike station coordinates and populating random customers.

* `entropy.py` contains the coding for building a covariance matrix from random sensor locations and calculating the (conditional) entropy of a joint normal distribution.

* `localvsgreedy.py` contains the code for combining the utility functions corresponding to instances  of set cover, facility location, and entropy into our experiments. We build a histogram of 100 random instances of each problem and compare the greedy and local search algorithms.


