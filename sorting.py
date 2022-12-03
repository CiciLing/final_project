"""
sorting.py
A demonstration of using evocomp to sort a list of numbers
"""
# Import libraries
import random as rnd
import pandas as pd
import numpy as np
import evo

# Global Variables
TAS, SECTIONS = pd.read_csv('data/tas.csv'), pd.read_csv('data/sections.csv')
MAX_COL = TAS['max_assigned']
TIME_COL = SECTIONS.daytime
MIN_COL = SECTIONS['min_ta']
TAS = TAS.iloc[:, 3:]

"""5 OBJECTIVE FUNCTIONS"""


def overallocation(sol):
    """Objective function: Identifies overallocation penalty"""
    return sum([np.sum(sol[i, :]) - np.array(MAX_COL)[i] for i in range(len(np.array(MAX_COL)))
                if np.sum(sol[i, :]) > np.array(MAX_COL)[i]])


def conflicts(sol):
    """Objective function: Identifies conflicts penalty"""
    return sum([1 for ta in range(len(pd.DataFrame(sol.tolist(), columns=TIME_COL.values.tolist())))
                if len(list(TIME_COL[sol[ta] == 1])) > len(set(TIME_COL[sol[ta] == 1]))])


def undersupport(sol):
    """Objective function: Identifies undersupport penalty"""
    sums = [pd.DataFrame(sol, columns=[MIN_COL.values.tolist()]).iloc[:, i].sum() for i in range(len(MIN_COL))]
    return sum([MIN_COL[i] - sums[i] for i in range(len(MIN_COL)) if MIN_COL[i] > sums[i]])


def unwilling(sol):
    """Objective function: Identifies unwilling penalty"""
    return len([1 for i in range(len(TAS)) for j in range(len(TAS.columns))
                if TAS.iloc[i, j] == "U" and sol[i, j] == 1])


def unpreferred(sol):
    """Objective function: Identifies unpreferred penalty"""
    return len([1 for i in range(len(TAS)) for j in range(len(TAS.columns))
                if TAS.iloc[i, j] == "W" and sol[i, j] == 1])


"""AGENT FUNCTIONS"""


def minimize_unwilling(solutions):
    """ Agent: replaces letter preferences with appropriate assignments (i.e. U = 0)"""
    return np.array([[0 if TAS.iloc[i, j] == "U" and solutions[0][i, j] == 1 else solutions[0][i, j]
                      for j in range(len(TAS.columns))] for i in range(len(TAS))])


def toggle(solutions):
    """ Agent: switches 0s and 1s for a random value in solution"""
    sol = solutions[0]
    i = rnd.randrange(0, sol.shape[0])
    j = rnd.randrange(0, sol.shape[1])
    sol[i, j] = 1 - sol[i, j]
    return sol


def swap_random_tas(sol) -> np.ndarray:
    """Agent function:"""
    # extract the solution from the list
    sol = sol[0]
    # get the index of two random TAs
    tas = np.random.choice(len(sol), 2)
    ta1, ta2 = tas[0], tas[1]
    # swap the two TAs
    sol[[ta1, ta2]] = sol[[ta2, ta1]]

    return sol



def fix_undersupport(sol) -> np.ndarray:
    """Agent function:"""
    # extract the solution from the List
    sol = sol[0]

    # number of TAs assigned to each lab is just the sum of each row
    labs_assigned = np.sum(sol, axis=0)

    # check to see if lab is undersupported
    undersupport = SECTIONS[:, 6] - labs_assigned

    def assign_ta(lab):
        """Helper function to assign a random lab to a TA."""
        # get the index of the labs assigned to the TA
        tas = np.where(sol[lab] == 0)[0]
        # get the index of a random Lab assigned to the TA
        ta = np.random.choice(tas)
        # remove the lab from the TA
        sol[ta][lab] = 1

    # toggle a random TA for each undersupported section
    [assign_ta(lab) for lab in np.where(undersupport > 0) [0]]
    return sol

def fix_overallocated_tas(sol) -> np.ndarray:
    """Agent function:."""
    # extract the solution from the list
    sol = sol[0]
    # get the number of labs assigned to eachiTA
    labs_assigned = np.sum(sol, axis=1)
    def unassign_lab(ta):
        """Helper function to unassign a random lab from a TA."""
        # get the index of the labs assigned to the TA
        labs = np.where(sol[ta] == 1)[0]
        # get the index of a random Lab assigned to the TA
        lab = np.random.choice(labs)
        # remove the lab from the TA
        sol[ta][lab] = 0

    # get the index of the TAs that are overallocated
    overallocated_tas = np.where(labs_assigned > MAX_COL)[0]

    #unassign a random lab from each overallocated TA
    [unassign_lab(ta) for ta in overallocated_tas]
    return sol


def main():
    # create population
    E = evo.Environment()

    # register the fitness criteria (objects)
    E.add_fitness_criteria("overallocation", overallocation)
    E.add_fitness_criteria("conflicts", conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unwilling", unwilling)
    E.add_fitness_criteria("unpreferred", unpreferred)

    # register all agents
    E.add_agent("minimize_unwilling", minimize_unwilling, 1)
    E.add_agent("toggle", toggle, 1)
    E.add_agent("swap_random_tas", swap_random_tas, 1)
    #E.add_agent("fix_undersupport", fix_undersupport, 1)
    E.add_agent("fix_overallocated_tas", fix_overallocated_tas, 1)

    # seed the population with an initial solution
    sol = np.random.choice([0, 1], size=(43, 17))
    E.add_solution(sol)
    # run the evolver
    E.evolve(5000000, dom=100, sync=1, status=10, time_limit=1200)

main()
