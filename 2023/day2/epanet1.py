import wntr
import matplotlib.pyplot as plt
# name of the input file
inp_file = "./data/Net1LPS.inp"
#create an EPANET network object
wn = wntr.network.WaterNetworkModel(inp_file)

# create a simulation object    
sim = wntr.sim.WNTRSimulator(wn)
# run the simulation and return the results
results = sim.run_sim()

# Analyze and visualize the results

for nodeID  in list(wn.nodes):
    maxp = results.node["pressure"].loc[:, nodeID].max()
    print(f"Max pressure at node ", nodeID, " is ", maxp, " m")
    
# plot pressure time series for all the nodes with legend nodeid    
results.node["pressure"].plot(legend=True, figsize=(10,6))
plt.ylabel("Pressure (m)")
plt.xlabel("Time (hours)")
# y axis log scale
plt.yscale("log")
# y axis ticks every 5 m    
plt.yticks(range(5, 100, 5))
# tick labels every tick
plt.xticks(range(5, 100, 5))
plt.show()
