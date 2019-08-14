import numpy as np
import wntr


inp_filename = './data/Net3LPS.inp'

wn = wntr.network.WaterNetworkModel(inp_filename) 
sim = wntr.sim.WNTRSimulator(wn, mode='PDD')
results = sim.run_sim()

pressure = results.node['pressure']
pressure_threshold = 21.09 # 30 psi
pressure_above_threshold = wntr.metrics.query(pressure, np.greater, pressure_threshold)

expected_demand = wntr.metrics.expected_demand(wn)
demand = results.node['demand']
wsa = wntr.metrics.water_service_availability(expected_demand, demand)
print("Water service availability: ", wsa.mean().mean())

head = results.node['head']
pump_flowrate = results.link['flowrate'].loc[:,wn.pump_name_list]
todini = wntr.metrics.todini_index(head, pressure, demand, pump_flowrate, wn, pressure_threshold)
print("Todini index:  ", todini.mean())

G = wn.get_graph()
flowrate = results.link['flowrate'].loc[12*3600,:]
G.weight_graph(link_attribute=flowrate)
entropy, system_entropy = wntr.metrics.entropy(G)