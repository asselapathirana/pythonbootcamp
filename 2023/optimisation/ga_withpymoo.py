from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from pb import display_helper
from pymoo.core.problem import Problem
from pymoo.factory import get_termination
import numpy as np

""" This is a helper function I have created to display the progress of the algorithm."""
monitor=display_helper.SOGraphMonitor(minimize=True)

"""Pymoo defines optimizatoin problem like this. You can find more details in the documentation.

n_var: number of variables
n_obj: number of objectives
xl: lower bound of the variables
xu: upper bound of the variables


"""
class leastSquare(Problem):

    def __init__(self):
        super().__init__(n_var=10, n_obj=1, xl=-5, xu=5)

    def _evaluate(self, x, out, *args, **kwargs):
        # important: here x is not a single solution but a set of solutions in a 2 dimensinoal array. 
        # So we need to use axis=1 to sum the squares of each solution.
        # e.g. out['F']=np.sum((x) ** 2, axis=1)
        # to make it easy to understand, I have used a for loop to calculate the sum of squares of each solution.
        # You can use the above line to replace the for loop.
        # out is the dictionary storing the fitness (and constraint) values. We don't have constraints in this problem 
        # So, we assign the fitness of the set of solutions to out['F']
        out['F'] = np.zeros(x.shape[0]) # The length of out['F'] is the number of solutions in x (x.shape[0]) 
        for i in range(x.shape[0]):
            out['F'][i]=np.sum((x[i]) ** 2)
     
# we create the problem object
problem = leastSquare()
# we create the algorithm object
algorithm = GA(
    pop_size=100,
    eliminate_duplicates=True)
# set a termination criterion for the algorithm based on number of generations
termination = get_termination("n_eval", 30000)
res = minimize(problem=problem,
               algorithm=algorithm,
               termination=termination,
               seed=1,
               verbose=False,
               callback=monitor)
print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
monitor.persist()