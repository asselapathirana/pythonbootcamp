"""
    ===============================================
    Helper module to run NSGAII algorithm of inspyred
    ===============================================
   
   .. Copyright 2022-2024 Assela Pathirana
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
    
    
    
"""

from ast import Call
import matplotlib
from time import time
matplotlib.use("QT5Agg")
import matplotlib.pyplot as plt
import numpy as np
import math
from random import Random
from pymoo.core.callback import Callback


#def update_graph():
#    """This is needed to give a graph a 'breather' during heavy calculations. It will reduce the graph freezing."""
#    plt.pause(.1)

class SOGraphMonitor(Callback):
    def __init__(self, minimize=True) -> None:
        super().__init__()
        self.n_evals = []
        self.minimize=minimize

        self.figure = plt.figure()
        ax = self.figure.add_subplot(111)
        #self.line2, = ax.plot(
        #    [], [], markerfacecolor="gray", marker="o", markersize=2, linestyle="None"
        #)  # Returns a tuple of line objects, thus the comma
        self.line1, = ax.plot(
            [], [], marker="o", markerfacecolor="blue", markersize=5
        )  # Returns a tuple of line objects, thus the comma
        self.fitness_history = []
        plt.ion()
        plt.show()

    def persist(self):
        plt.ioff()
        plt.show()

    def notify(self, algorithm):
        self.n_evals.append(algorithm.evaluator.n_eval)
        population_=algorithm.pop.get("F")
        self.fitness_history.append(population_.min() if self.minimize else population_.max())
        print(f"Running: evaluation={algorithm.evaluator.n_eval}")

        x1_data=self.n_evals
        y1_data=self.fitness_history
        self.line1.set_data(x1_data, y1_data)
        self.figure.canvas.draw()
        # adjust limits if new data goes beyond bounds
        #x1all = self.fitness_history[0]
        #y1all = self.fitness_history[1]
        # if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1all)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])
        # adjust limits if new data goes beyond bounds
        # if np.min(x1all)<=line1.axes.get_xlim()[0] or np.max(x1all)>=line1.axes.get_xlim()[1]:
        plt.xlim([np.min(x1_data) - np.std(x1_data), np.max(x1_data) + np.std(x1_data)])
        self.figure.canvas.flush_events()
        #input()


class MOGraphMonitor(Callback):

    def __init__(self) -> None:
        super().__init__()
        self.n_evals = []

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

    def notify(self, algorithm):
        self.n_evals.append(algorithm.evaluator.n_eval)
        population_=algorithm.pop.get("F")
        population=population_[population_[:, 0].argsort()]
        print(f"Running: evaluation={algorithm.evaluator.n_eval}, midfitness={population[25]}")

        x1_data=population[:,0]
        y1_data=population[:,1]
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
        #input()