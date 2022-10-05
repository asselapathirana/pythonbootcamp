# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 14:17:12 2022

@author: ifa001
"""

import wntr

CTRITP = 20
STEP = 0.005
LINK='10'

# Create a water network model
inp_file = 'data/Net1.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

# Finding diameter of pipe LINK
pipe10 = wn.get_link(LINK)
print(f"Original diameter of Pipe {LINK} is {pipe10.diameter:0.2f}(m) ")
i= 1
origdia=pipe10.diameter

# Changing the diameter of pipe LINK

nsteps=int(origdia/STEP)
for i in range(nsteps):
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    press = results.node["pressure"].loc[:]
    minpress = press.min()[:9] #excluding the reservoir
    minp = min(minpress)
    #print(pipe10.diameter, minp) - To see the progress of the loop
    if minp < CTRITP:
        break
    olddia = pipe10.diameter
    pipe10.diameter = origdia-STEP*i

msg=f"New diameter of pipe {LINK} {olddia:0.2f} (m) "
print(msg)

