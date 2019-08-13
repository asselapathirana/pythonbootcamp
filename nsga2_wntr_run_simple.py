import math
import wntr
from pb.nsgaII_helper.nsgaII_helper import NSGAII_run, Pareto, Bounder, plt
import os


NVARS = 10
valrange=[.1, 1.0]
outputd="output"


if not os.path.exists(outputd):
    os.makedirs(outputd)



#initialize 
inpfile='Net1.inp'
wn = wntr.network.WaterNetworkModel(inpfile) 
orig_diam = [wn.get_link("11").diameter, 
             wn.get_link("12").diameter, 
             wn.get_link("111").diameter, 
             wn.get_link("112").diameter, 
             wn.get_link("113").diameter, 
             wn.get_link("21").diameter, 
             wn.get_link("22").diameter, 
             wn.get_link("121").diameter, 
             wn.get_link("122").diameter, 
             wn.get_link("31").diameter, 
             ]
print("init done", orig_diam)

def mygenerator(random, args):
    return [random.uniform(*valrange) for x in range(NVARS)]

def evaluate(factors, number):
    wn = wntr.network.WaterNetworkModel(inpfile) 
    vals = [a*b for a,b in zip(factors, orig_diam)]
    [wn.get_link("11").diameter, 
                 wn.get_link("12").diameter, 
                 wn.get_link("111").diameter, 
                 wn.get_link("112").diameter, 
                 wn.get_link("113").diameter, 
                 wn.get_link("21").diameter, 
                 wn.get_link("22").diameter, 
                 wn.get_link("121").diameter, 
                 wn.get_link("122").diameter, 
                 wn.get_link("31").diameter, 
                 ] = vals
    sim = wntr.sim.WNTRSimulator(wn, mode='PDD')
    results = sim.run_sim(solver_options=dict(MAXITER=500, TOL=1.e-4), convergence_error=True)
    pressure = results.node['pressure']
    pressure_threshold = 21.09 # 30 psi
    expected_demand = wntr.metrics.expected_demand(wn)[wn.junction_name_list]
    demand = results.node['demand'][wn.junction_name_list]
    head = results.node['head']
    pump_flowrate = results.link['flowrate'].loc[:,wn.pump_name_list]
    wsa = demand.sum().sum()/expected_demand.sum().sum()
    cost = wntr.metrics.economic.annual_network_cost(wn)
    
    # now save the files (so that we can examine them later too!)
    inpname='{0}{1}CANDIDATE_{2:03d}.inp'.format(outputd,os.sep,number)
    resfile='{0}{1}CANDIDATE_{2:03d}.txt'.format(outputd,os.sep,number)    
    wn.write_inpfile(inpname)
    with open(resfile,'w') as ff:
        ff.write("Cost ($/y): {}, 1-ADF (-): {}".format(cost,1-wsa))
    return cost, 1-wsa
    

def myevaluator(candidates, args):
    fitness = []
    for i,cc in enumerate(candidates):
        fail = False
        try:
           
            rr = evaluate(cc,i)
        except Exception as e:
            print ("\n______________________________________________\n"+str(e)+'\n__________________________________________\n')
            fail=True
        if fail or math.isnan(rr[0]) or math.isnan(rr[1]):
            rr=[419929,1.0] # only 1-0.6 is lost to leakage and supply ratio is 0!! 
        fitness.append(Pareto(rr))
        plt.pause(.1)
        print (rr, ": ", cc)
    return fitness


def main(prng=None, display=False):
    # custom problem
    generator=mygenerator
    evaluator=myevaluator
    bounder=Bounder(*valrange)    
    NSGAII_run(generator, evaluator, bounder, prng, maximize=False, pop_size=4, max_generations=100, display=True)


if __name__ == '__main__':
    main(display=True)    