import math
import wntr
from pb.nsgaII_helper.nsgaII_helper import NSGAII_run, update_graph
from inspyred.ec.emo import Pareto  # Pack fitness values to this
from inspyred.ec import Bounder  # Useful to specify variable boundaries
import os # need this for file path handling
import shutil # need to remove an entire directory


valrange=[.1, 1.0] # range of each variables? 
outputd="output" # directory to write output to 
inpfile='Net1.inp'
# list pipe ids to change
pipes_to_change = ['11', '12', '111', '112', '113', '21', '22', '121', '122', '31']
NVARS = len(pipes_to_change) # how many variables do you want to change


if not os.path.exists(outputd): # create output directory if not there
    os.makedirs(outputd)
else:
    filelist = [ ff for ff in os.listdir(outputd) ]
    for fil in filelist:
        os.remove(os.path.join(outputd, fil))    


resfile='{0}{1}results.txt'.format(outputd,os.sep) 
TBL="{:>10}{:>25} {:>25} {:>25}\n"
with open(resfile, 'w+') as ff:
    ff.write(TBL.format("Number","INP file", "Cost (US$/y)", "(1-ADF)"))

wn = wntr.network.WaterNetworkModel(inpfile) 
# keep the original diameters saved. 
orig_diam = [wn.get_link(id).diameter for id in pipes_to_change] 

def mygenerator(random, args): 
    """Generator"""
    return [random.uniform(*valrange) for x in range(NVARS)]

def evaluate(factors, number):
    """Given a list of diameters, how to calculate the two objective functions"""
    wn = wntr.network.WaterNetworkModel(inpfile) # open the input file
    # convert the variable to a diameter value
    vals = [a*b for a,b in zip(factors, orig_diam)] 
    # now change the diameters in the network. 
    for id, diam in zip(pipes_to_change, vals):
        wn.get_link(id).diameter=diam 
    # now create a simulation using PDD mode
    sim = wntr.sim.WNTRSimulator(wn, mode='PDD')
    # slacken the convergence criteria a bit - to save some time
    results = sim.run_sim(solver_options=dict(MAXITER=500, TOL=1.e-2), convergence_error=False)
    if (results.error_code==2):
            print ("\nHydrfaulic analysis failed to converge!\n")
    # objective 1 is : annualized cost in US$/year
    cost = wntr.metrics.economic.annual_network_cost(wn)
    
    expected_demand = wntr.metrics.expected_demand(wn)[wn.junction_name_list]
    demand = results.node['demand'][wn.junction_name_list]
    #objective 2 is 1-adf
    adf = demand.sum().sum()/expected_demand.sum().sum()
   
    # now save the files (so that we can examine them later too!)
    inpname='{0}{1}CANDIDATE_{2:03d}.inp'.format(outputd,os.sep,number)
    wn.write_inpfile(inpname)
    # write objective values to the result file
    with open(resfile,'a') as ff:
        ff.write(TBL.format(number,inpname, "{:.9f}".format(cost), '{:.9f}'.format(1-adf)))
    return cost, 1-adf

    

def myevaluator(candidates, args):
    fitness = []
    for i,cc in enumerate(candidates):
        rr = evaluate(cc,i)
        fitness.append(Pareto(rr))
        update_graph()
        print (rr, ": ", cc)
    return fitness


def main(prng=None, display=False):
    # custom problem
    generator=mygenerator
    evaluator=myevaluator
    bounder=Bounder(*valrange)    
    NSGAII_run(generator, evaluator, bounder, prng, maximize=False, pop_size=4, max_generations=10, display=True)


if __name__ == '__main__':
    main(display=True)    