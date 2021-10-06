# Copyright (c) 2021 Assela Pathirana
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
import wntr

def runSet(network, diameter, link, node, PDD=False ):
    wn = wntr.network.WaterNetworkModel(network) 
    if PDD: 
        wn.options.hydraulic.demand_model = 'PDD'
    else:
        wn.options.hydraulic.demand_model = 'DD'
    plink=wn.get_link(link)
    plink.diameter=diameter
    sim = wntr.sim.EpanetSimulator(wn)
    results=sim.run_sim()
    mp= results.node['pressure'][node].min()
    
    return mp

if __name__ == '__main__':
    res=runSet('Net3LPS.inp', 0.08, '137', '131', PDD=True)
    print(res)