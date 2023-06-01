# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 12:12:03 2022

@author: ifa001
"""

import pyswmm as ps

from swmm.toolkit.shared_enum import LinkAttribute

sim = ps.Simulation("swmm5Example.inp")
sim.execute()

with ps.Output('swmm5Example.out') as out:
    ts = out.link_series("T5", LinkAttribute.FLOW_RATE)
    flows = ts.values()
    maxv = max(flows)
    print(f"The maximum flow in T5 is {maxv:.2f}")