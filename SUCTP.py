"""
This script is designed to solve the Stochastic University Course TImetabling Problem

Problem description:
There is a set of courses that must be taught within 
a timeframework usually 1 week.

There is also a set of professor who has availability 
and skills to teach a subset of objects that

Besides, the demand of each course is assumed stochastic
following a given probability distribution

The objective function is to minimize the cost of
assigning professor to subjects as well as a penalazation
cost, associated to leave student out of a lesson in a given timeslot

The problem is solved directly using cplex solver, but we also implement the
the GAPM (Generalized adaptive partition method) 
developed by Ramirez-Pico and Moreno
"""

import cplex
import numpy as np

# Here we need to create a set of functions which 
# are able to generate random instances


def full_suctp(W, M, G, O, H, A, C: dict, Cf, D, p, partition):
    """
    params:
    W: int N° max of students per session
    M: int Maximum number of sessions allowed simultaneously
    G: array Max number of sessions each professor might teach along the time horizon
    O: array Max number of sessions of a certain subjects
    H: 2d array Binary indicator if a lecturer might teach a given subject
    A: 2d array Availability of teacher at each timeslot 
    C: dict which keay are var names and values are 
       costs of assigning a lecturer on a give timeslot
    Cf: float Penalization cost
    D: 3d array Demand of subject at time t for a given scenario
    p: array of probabilities for each scenario
    partition: 2d array containing element of current partition
    """
    suctp_env = cplex.Cplex()
    # Important data
    periods = len(A[0])
    n_subjects = len(O)
    n_prof = len(A)
    #the number of scenarios will depend on number of element in the current partition
    scenarios = len(partition)

    #add variables to the model
    #first stage variables
    suctp_env.variables.add(names = C.keys(), types=suctp_env.variables.type.binary, obj=C.values())
    #second-stage variables
    y_names = ["f_" + str(i) + "_" + str(t) + "_" + str(s) for i in range(n_subjects) 
                for t in range(periods) for s in range(scenarios)]
    suctp_env.variables.add(names = y_names, types=suctp_env.variables.type.continuous, obj = Cf)

    #add the constarinst of the model
    