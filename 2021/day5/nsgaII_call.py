# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 15:36:48 2021

@author: apa
"""
import math
from pb.nsgaII_helper.nsgaII_helper import NSGAII_run
from inspyred.ec.emo import Pareto  # Pack fitness values to this
def mygenerator(random, args):
    return [
        random.uniform(-5.0, 5.0) for x in range(3)
    ]  # initial values of the variables. Kursawe(3) problem has 3 variables x1, x2, x3
def myevaluator(candidates, args):
    fitness = []
    for cc in candidates:
        f1 = sum(
            [
                -10 * math.exp(-0.2 * math.sqrt(cc[i] ** 2 + cc[i + 1] ** 2))
                for i in range(len(cc) - 1)
            ]
        )
        f2 = sum([math.pow(abs(x), 0.8) + 5 * math.sin(x) ** 3 for x in cc])
        pp = Pareto(
            [f1, f2]
        )  # Pareto is the special data type provided by inspyred libarary
        fitness.append(pp)  # append it to the list called fitness
    return (
        fitness
    )  # return fitness which is the  set fitness values for all candidates.
def mybounder(candidate, args):
    for ii in range(len(candidate)): # each diameter value
        # if value is less than lower bound make it = lowerbound
        # if value is greater than upper bound make it = upperbound
        candidate[ii]=min(max(candidate[ii], -5.0), 5.0) 
    return candidate
def main():
    # now run the optimizer
    NSGAII_run(
        generator=mygenerator,
        evaluator=myevaluator,
        bounder=mybounder,
        prng=None,
        maximize=False,
        pop_size=200,
        max_generations=200,
        display=True,
    )
if __name__ == "__main__":
    main()