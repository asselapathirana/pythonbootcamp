# Copyright (c) 2021 Assela Pathirana
# 
# This software is released under the MIT License.
# https:#opensource.org/licenses/MIT

"""
The following example demonstrates how to import WNTR, generate a water network 
model from an INP file, simulate hydraulics, and plot simulation results on the network.
"""
import wntr

# Create a water network model
inp_file = 'data/Net3LPS.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

# Simulate hydraulics
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()

pressures = results.node['pressure']

# pressures is a pandas dataframe with node ids a column headers and time (in ms) as
# index
#first get max pressure in each node
nmaxp=pressures.max()

# this is a series with index as id of each node and value as max pressure 
# of each node. 
# what is the maximum value of pressure? 
maxp=nmaxp.max()
# relevent node id
maxpid=nmaxp.idxmax()

# what time? 
# get the pressure at maxpid
pp = pressures[maxpid]
#time when max
mt = pp.idxmax()
print("Maximum pressure of ", maxp, "occurs at the node", maxpid, "at time ", mt/3600, " hours.")