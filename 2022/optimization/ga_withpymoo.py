from gc import callbacks
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pb import display_helper

problem = get_problem("Zakharov")
monitor=display_helper.SOGraphMonitor(minimize=True)

algorithm = GA(
    pop_size=100,
    eliminate_duplicates=True)

res = minimize(problem,
               algorithm,
               seed=1,
               verbose=False,
               callback=monitor)
print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
monitor.persist()