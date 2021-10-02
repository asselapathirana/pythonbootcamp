"""
=====================================================================================================
An example script showcasting the use of wntr library
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

# Run a Pressure Dependant Demand simulation 
wn = wntr.network.WaterNetworkModel(inp_filename) 
sim = wntr.sim.WNTRSimulator(wn, mode='PDD')
results = sim.run_sim()

pressure = results.node['pressure']
pressure_threshold = 20 # m head
pressure_above_threshold = wntr.metrics.query(pressure, np.greater, pressure_threshold)

# Calculate ADF 
expected_demand = wntr.metrics.expected_demand(wn)
demand = results.node['demand']
wsa = wntr.metrics.water_service_availability(expected_demand, demand)
print(FORMAT.format("Water service availability",wsa.mean().mean()))

head = results.node['head']
pump_flowrate = results.link['flowrate'].loc[:,wn.pump_name_list]
todini = wntr.metrics.todini_index(head, pressure, demand, pump_flowrate, wn, pressure_threshold)
print(FORMAT.format("Todini index", todini.mean()))

G = wn.get_graph()
flowrate = results.link['flowrate'].loc[12*3600,:]
G.weight_graph(link_attribute=flowrate)
entropy, system_entropy = wntr.metrics.entropy(G)