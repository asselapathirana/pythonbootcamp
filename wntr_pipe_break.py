"""
=====================================================================================================
An example script showcasting the use of wntr library:
Available demand fraction:
1. Normal operation
2. Pipe burst (full burst) - no closure
2. Pipe closed
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

import numpy as np
import wntr

# Input (epanet network format) file name
inp_filename = './data/Net3LPS.inp'
FORMAT = "{:>50} : {:10.4f}"

def water_service_avail(wn):
    # Run a Pressure Dependant Demand simulation 
    sim = wntr.sim.WNTRSimulator(wn, mode='PDD')
    results = sim.run_sim()    
    # Calculate ADF 
    expected_demand = wntr.metrics.expected_demand(wn)
    demand = results.node['demand']
    wsa = wntr.metrics.water_service_availability(expected_demand, demand)
    print(FORMAT.format("Water service availability",wsa.mean().mean()))
    
wn = wntr.network.WaterNetworkModel(inp_filename) 
print("Before break:")
water_service_avail(wn)
wn.reset_initial_values()
# first consider a broken pipe (actively leaking)
wn = wntr.morph.split_pipe(wn, '175', '175_B', '175_leak_node')
leak_node = wn.get_node('175_leak_node')
diameter=wn.get_link("175").diameter
leak_node.add_leak(wn, area=diameter, start_time=0, end_time=None)
print("After break:")
water_service_avail(wn)
wn.reset_initial_values()

link=wn.get_link("175")
link.diameter=0.001 # neglegible diameter 1 mm
print("After closure:")
water_service_avail(wn)
