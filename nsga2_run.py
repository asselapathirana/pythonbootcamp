"""
=====================================================================================================
Following code runs the Kursawe(3) problem of minimization. For clarity, all the necessary elements 
(e.g. generator, evaluator, etc) are reproduced here (mygenerator etc.) rather than calling from 
the inspyred library. 
=====================================================================================================
   
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

"""

import math
from pb.nsgaII_helper.nsgaII_helper import NSGAII_run
from inspyred.ec.emo import Pareto  # Pack fitness values to this


def mygenerator(random, args):
    """Generate the first population. Random values for each of x1, x2, x3 variables!"""
    return [
        random.uniform(-5.0, 5.0) for x in range(3)
    ]  # initial values of the variables. Kursawe(3) problem has 3 variables x1, x2, x3


def myevaluator(candidates, args):
    """given a set of candidates calculate objective 1 and 2 (if 2 objectives, more if you have more objectives). 
    These are teh fitness values. Put each pair in Pareto object provided by inspyred. 
    Return as a list (same order as candidates! )
    """
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
