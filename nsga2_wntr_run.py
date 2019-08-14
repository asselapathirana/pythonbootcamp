from random import Random
from time import time
import math

from pb.nsgaII_helper.nsgaII_helper import _graph_monitor, nsgaII, Pareto, Bounder, plt
from pb.wntr import  simulate_with_leakage as sl

NVARS = 5
valrange=[.01, 1.0]


#initialize 
inpfile='Net3LPS.inp'
wl=sl.wntr_leakage(inpfile)
print("1")
wl.add_leaks(200/1.e6)  # x sq. mm (x/1.e6 sq.m in the equation - remember WNTR users m) for each 1 km of pipe)
orig_diam = [wl.wnl.get_link('101').diameter, wl.wnl.get_link('60').diameter, wl.wnl.get_link('20').diameter, 
        wl.wnl.get_link('40').diameter, wl.wnl.get_link('50').diameter ]
print("init done", orig_diam)
def mygenerator(random, args):
    return [random.uniform(*valrange) for x in range(NVARS)]

def myevaluator(candidates, args):
    fitness = []
    for cc in candidates:
        wl.load() # reset. This is important before each set of simulations. 
        vals = [a*b for a,b in zip(cc, orig_diam)]
        wl.wnl.get_link('101').diameter, wl.wnl.get_link('60').diameter, wl.wnl.get_link('20').diameter, \
        wl.wnl.get_link('40').diameter, wl.wnl.get_link('50').diameter = vals
        fail=False
        try:
           
            rr = wl.adf_leak()
        except Exception as e:
            print ("______________________________________________\n"+str(e)+'__________________________________________\n')
            fail=True
        if fail or math.isnan(rr[0]) or math.isnan(rr[1]):
            rr=[0.0,.6] # only 1-0.6 is lost to leakage and supply ratio is 0!! 
        fitness.append(Pareto(rr))
        plt.pause(.1)
        
        print (rr, ": ", vals)
    return fitness


def main(prng=None, display=False):
    if prng is None:
        prng = Random()
        prng.seed(time()) 
        
    
    
    # custom problem
    generator=mygenerator
    evaluator=myevaluator
    bounder=Bounder(*valrange)    
    nsgaII.run(prng, generator, evaluator, bounder, maximize=True, pop_size=100, max_generations=100)


if __name__ == '__main__':
    main(display=True)    