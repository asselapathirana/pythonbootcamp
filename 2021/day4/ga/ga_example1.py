from random import Random
from time import time
from math import cos
from math import pi
from inspyred import ec
from inspyred.ec import terminators, observers
import wntr
import sys

network="Net1.inp"
pcrit=20
wn = wntr.network.WaterNetworkModel(network) 
wn.options.hydraulic.demand_model = 'PDD'
ids=['10', '110', '11', '12', '112']
lens=[wn.get_link(x).length for x in ids]
def generate_dia(random, args):
    size = len(ids)
    return [random.uniform(.1, .5) for i in range(size)]

def evaluate(candidates, args):
    fitness = []
    for cs in candidates:
        fit=calculate_fitness(cs)
        fitness.append(fit)
    return fitness

def calculate_fitness(cs):
    fit = sum( [ x*y*50 for x,y in zip(cs,lens)])
    for x,y in zip(ids, cs):
        wn.get_link(x).diameter=y 
        try:
            sim = wntr.sim.EpanetSimulator(wn)
            results=sim.run_sim()
            minp=results.node['pressure'].min().min()
            if (minp-pcrit)<0:
                fit=fit+100000000000*(-1)*(minp-pcrit)
        except:
            print("A problem at ", cs)
            fit=sys.float_info.max
    return fit

def my_observer(population, num_generations, num_evaluations, args):
    best = min(population)
    print('{0:6} -- {1} : {2}'.format(num_generations, 
                                      best.fitness, 
                                      str(best.candidate)))



rand = Random()
rand.seed(int(time()))
es = ec.ES(rand)
es.terminator = terminators.evaluation_termination
es.observer = my_observer
final_pop = es.evolve(generator=generate_dia,
                      evaluator=evaluate,
                      pop_size=10,
                      maximize=False,
                      bounder=ec.Bounder(.1, .5),
                      max_evaluations=1000,
                      mutation_rate=0.025)
