from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pb import display_helper

problem = get_problem("sphere")

algorithm = GA(pop_size=100)
monitor=display_helper.SOGraphMonitor(minimize=True)
res = minimize(problem,
               algorithm,
               ('n_gen', 50),
               seed=1,
               callback=monitor,
               verbose=True)
monitor.persist()