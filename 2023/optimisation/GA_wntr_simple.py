# Copyright (c) 2021 Assela Pathirana
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

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
   
from gc import callbacks
import wntr
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.optimize import minimize
from pymoo.termination import get_termination
import os # need this for file path handling
from pb import display_helper

# Following are GLOBAL variables. 
# It is not a good practice to have too many global variables 
# In fact good program design allows to avoid them (almost) fully. 
valrange=[.05, 1.0] # range of each variables? 
outputd="output" # directory to write output to 
inpfile='./data/Net1x.inp'
# list ids of pipes to change
pipes_to_change = ['10', '11', '12', '21', '22', '31', '111', '112', '113']
NVARS = len(pipes_to_change) # how many variables do you want to change
MINADF=0.75 # minimum ADF value to be considered
# pentalty to be added to cost if ADF is less than MINADF
LN=1.e12
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
    """Given a list of diameters, a single objective function is evaluated.
        objective: minimize operational cost with subject to a constraint on ADF 
        if ADF < minADF, we add a penalty to the cost function (so that 'cost' will be very high. )
    """
    wn = wntr.network.WaterNetworkModel(inpfile) # open the input file
    # convert the variable to a diameter value
    vals = [a*b for a,b in zip(factors, orig_diam)] 
    # now change the diameters in the network. 
    for id, diam in zip(pipes_to_change, vals):
        wn.get_link(id).diameter=diam 
    # now create a simulation using PDD mode
    wn.options.hydraulic.demand_model = 'PDA'
    sim = wntr.sim.EpanetSimulator(wn)
    # slacken the convergence criteria a bit - to save some time
    results = sim.run_sim(version=2.2)# solver_options=dict(MAXITER=2000, TOL=1.e-2), convergence_error=False)
    if (results.error_code==2):
            print ("\nHydrfaulic analysis failed to converge!\n")
    # objective 1 is : annualized cost in US$/year
    cost = wntr.metrics.economic.annual_network_cost(wn)
    
    expected_demand = wntr.metrics.expected_demand(wn)[wn.junction_name_list]
    demand = results.node['demand'][wn.junction_name_list]
    #objective 2 is 1-adf
    adf = demand.sum().sum()/expected_demand.sum().sum()
    #adf=1 if adf > 1.0 else adf # Remove > 1 adf (sometimes it can happen!)
    
    # now save the files (so that we can examine them later too!)
    inpname=f'{outputd}{os.sep}CANDIDATE_{number:03d}.inp'
    wntr.network.io.write_inpfile(wn, inpname)
    # write objective values to the result file
    with open(resfile,'a') as ff:
        ff.write(TBL.format(number,inpname, "{:.9f}".format(cost), '{:.9f}'.format(1-adf)))
    LNADF= 0.0 if adf > MINADF else LN*(MINADF-adf)
    return cost + LNADF


def write_heading():
    # write heading for results file
    with open(resfile, 'w+') as ff:
        ff.write(TBL.format("Number","INP file", "Cost (US$/y)", "(1-ADF)"))    

class PipeProblem(ElementwiseProblem):

    def __init__(self):
        super().__init__(n_var=NVARS,
                         n_obj=1,
                         n_ieq_constr=0,
                         xl=valrange[0],
                         xu=valrange[1])
        self.n=0

    def _evaluate(self, x, out, *args, **kwargs):
        self.n+=1
        out["F"] = evaluate(x, self.n)
        #out["G"] = [x-valrange[0],valrange[1]-x] 



def main(prng=None, display=False):
    clean()
    write_heading()
    # run! 
    termination = get_termination("n_gen", 200)
    problem=PipeProblem()
    algorithm = GA(
        pop_size=40,
        )
    monitor=display_helper.SOGraphMonitor()
    res = minimize(problem,
               algorithm,
               termination,
               seed=1,
               save_history=True,
               verbose=True, 
               callback=monitor)
    monitor.persist()
    



if __name__ == '__main__':
    main(display=True)    