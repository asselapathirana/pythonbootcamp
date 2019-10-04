"""
    ===============================================
    A prototype example of running multi(two)-objective optimization problem using 
   wntr and inspyred libraries
    ===============================================
    
    This example is a design problem and claculates the relationship betweek 
    (1-ADF), i.e., impact on supply and cost of pipes. 
        In a given water distribution network, change specified pipes
        
        - for cost we use wntr.metrics.economic.annual_network_cost() function
        without any changes
        - for ADF we use the ratio: total demand in the system 
        (in the junction list) over expected demand (wntr.metrics.expected_demand) 
    
   
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
   
import wntr
from pb.nsgaII_helper.nsgaII_helper import NSGAII_run, update_graph
from inspyred.ec.emo import Pareto  # Pack fitness values to this
import os # need this for file path handling

# Following are GLOBAL variables. 
# It is not a good practice to have too many global variables 
# In fact good program design allows to avoid them (almost) fully. 
valrange=[.1, 1.0] # range of each variables? 
outputd="output" # directory to write output to 
inpfile='./data/Net1.inp'
# list ids of pipes to change
pipes_to_change = ['11', '12', '111', '112', '113', '21', '22', '121', '122', '31']
NVARS = len(pipes_to_change) # how many variables do you want to change

resfile='{0}{1}results.txt'.format(outputd,os.sep) # results file
TBL="{:>10}{:>25} {:>25} {:>25}\n" # nice printing
# original diameters of the pipes
orig_diam = [wntr.network.WaterNetworkModel(inpfile).get_link(id).diameter for id in pipes_to_change] 
# end of GLOBAL variables 

def clean():
    """ Clean up the directory by deleting any existing output files"""
    if not os.path.exists(outputd): # create output directory if not there
        os.makedirs(outputd)
    else:
        filelist = [ ff for ff in os.listdir(outputd) ]
        for fil in filelist:
            os.remove(os.path.join(outputd, fil))    


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

def mybounder(candidate, args):
    for ii in range(len(candidate)): # each diameter value
        # if value is less than lower bound make it = lowerbound
        # if value is greater than upper bound make it = upperbound
        candidate[ii]=min(max(candidate[ii], valrange[0]), valrange[1]) 
    return candidate

def write_heading():
    # write heading for results file
    with open(resfile, 'w+') as ff:
        ff.write(TBL.format("Number","INP file", "Cost (US$/y)", "(1-ADF)"))    

def main(prng=None, display=False):
    clean()
    write_heading()
    # run! 
    NSGAII_run(generator=mygenerator, evaluator=myevaluator, bounder=mybounder, prng=prng, maximize=False, pop_size=4, max_generations=10, display=True)


if __name__ == '__main__':
    main(display=True)    