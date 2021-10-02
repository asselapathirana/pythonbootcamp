"""
    ===============================================
    Helper module to run NSGAII algorithm of inspyred
    ===============================================
   
   .. Copyright 2019 Assela Pathirana

    .. This program is free software: you can redistribute it and/or modify
       it under the terms of the GNU General Public License as published by
       the Free Software Foundation, either version 3 of the License, or
       (at your option) any later version.

    .. This program is distributed in the hope that it will be useful,
       but WITHOUT ANY WARRANTY; without even the implied warranty of
       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
       GNU General Public License for more details.

    .. You should have received a copy of the GNU General Public License
       along with this program.  If not, see <http://www.gnu.org/licenses/>.
       
    .. author:: Assela Pathirana <assela@pathirana.net>
    
    
Example code::

Following code runs the Kursawe(3) problem of minimization. For clarity, all the necessary elements 
(e.g. generator, evaluator, etc) are reproduced here (mygenerator etc.) rather than calling from the inspyred library. 

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
        pop_size=100,
        max_generations=100,
        display=True,
    )


if __name__ == "__main__":
    main()
    
"""

import matplotlib
from time import time
matplotlib.use("QT5Agg")
import matplotlib.pyplot as plt
import numpy as np
import math
from random import Random
import inspyred
from inspyred.ec.emo import Pareto
from inspyred.ec import Bounder


def update_graph():
    """This is needed to give a graph a 'breather' during heavy calculations. It will reduce the graph freezing."""
    plt.pause(.1)

def NSGAII_run(
    generator,
    evaluator,
    bounder,
    prng=None,
    maximize=True,
    pop_size=100,
    max_generations=100,
    display=False
):
    if prng is None:
        prng = Random()
        prng.seed(time())     
    
    ea = inspyred.ec.emo.NSGA2(prng)
    ea.variator = [
        inspyred.ec.variators.blend_crossover,
        inspyred.ec.variators.gaussian_mutation,
    ]
    ea.terminator = inspyred.ec.terminators.generation_termination
    if display:
        monitor = _graph_monitor()
    else:
        monitor = _text_monitor()
    ea.observer = monitor.nsgaII_observer
    ea.evolve(
        generator=generator,
        evaluator=evaluator,
        pop_size=pop_size,
        bounder=bounder,
        maximize=maximize,
        max_generations=max_generations,
    )
    if display:
        monitor.persist()
        

class _text_monitor():
    
    def nsgaII_observer(self, population, num_generations, num_evaluations, args):
        print ("N={}: {}".format(num_evaluations, population))


class _graph_monitor:
    """A graph to monitor NSGAII progress"""
    def __init__(self):
        self.figure = plt.figure()
        ax = self.figure.add_subplot(111)
        self.line2, = ax.plot(
            [], [], markerfacecolor="gray", marker="o", markersize=2, linestyle="None"
        )  # Returns a tuple of line objects, thus the comma
        self.line1, = ax.plot(
            [], [], marker="o", markerfacecolor="blue", markersize=5
        )  # Returns a tuple of line objects, thus the comma
        self.fitness_history = [np.array([]), np.array([])]
        plt.ion()
        plt.show()

    def persist(self):
        plt.ioff()
        plt.show()

    def nsgaII_observer(self, population, num_generations, num_evaluations, args):
        population = sorted(population, key=lambda f: f.fitness[0])
        print(num_generations, ":", population)
        x1_data, y1_data = zip(*[p.fitness for p in population])
        self.line1.set_data(x1_data, y1_data)
        self.line2.set_data(*self.fitness_history)

        self.fitness_history[0] = np.append(self.fitness_history[0], x1_data)
        self.fitness_history[1] = np.append(self.fitness_history[1], y1_data)

        self.figure.canvas.draw()
        # adjust limits if new data goes beyond bounds
        x1all = self.fitness_history[0]
        y1all = self.fitness_history[1]
        # if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1all)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1all) - np.std(y1all), np.max(y1all) + np.std(y1all)])
        # adjust limits if new data goes beyond bounds
        # if np.min(x1all)<=line1.axes.get_xlim()[0] or np.max(x1all)>=line1.axes.get_xlim()[1]:
        plt.xlim([np.min(x1all) - np.std(x1all), np.max(x1all) + np.std(x1all)])
        self.figure.canvas.flush_events()
