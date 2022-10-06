from gc import callbacks
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pb import display_helper
problem = get_problem("Kursawe")

algorithm = NSGA2(pop_size=200)
dh=display_helper.MOGraphMonitor()
res = minimize(problem,
               algorithm,
               ('n_gen', 2000),
               seed=10,
               verbose=False,
               callback=dh)
dh.persist()