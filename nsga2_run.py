import math
from pb.nsgaII_helper.nsgaII_helper import NSGAII_run
from inspyred.ec.emo import Pareto  # Pack fitness values to this
from inspyred.ec import Bounder  # Useful to specify variable boundaries


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


def main():
    mybounder = Bounder(
        [-5.0, -5.0, -5.0], [5.0, 5.0, 5.0]
    )  # each variable x1, x2, x3 can have valid values from -5 to 5
    # now run the optimizer
    NSGAII_run(
        generator=mygenerator,
        evaluator=myevaluator,
        bounder=mybounder,
        prng=None,
        maximize=False,
        pop_size=100,
        max_generations=10,
        display=True,
    )


if __name__ == "__main__":
    main()
