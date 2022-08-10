# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:44:40 2021

@author: apa
"""
import wntr
from matplotlib import pyplot as plt
# Create a water network model
inp_file = 'data/Net3LPS_LD.inp'
wn = wntr.network.WaterNetworkModel(inp_file) 
wn.options.hydraulic.demand_model = 'PDD'
sim=wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()
p151 = results.node['pressure'].loc[:,'151']
d151 = results.node['demand'].loc[:,'151']*1000

# define a subplot with two rows
fig, axx = plt.subplots(2,1)

ax1=p151.plot(ax=axx[0])
ax1.set_xlabel("time (s)")
ax1.set_ylabel("Pressure Head (m)")

ax=d151.plot(ax=axx[1])
ax.set_xlabel("time (s)")
ax.set_ylabel("Demand (l/s)")
plt.show()
