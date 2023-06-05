import wntr
import matplotlib.pyplot as plt
# open network file
inp_file = "./data/Net1LPS.inp"
# create a water network model object
wn = wntr.network.WaterNetworkModel(inp_file)
# create a simulation object
sim = wntr.sim.WNTRSimulator(wn)
# run the simulation and return the results
results = sim.run_sim()
# get the list of nodes
node_list = list(wn.nodes)
print("Node list: ", node_list)

# get the maximum pressure at each node
for nodeID  in node_list:
    maxp = results.node["pressure"].loc[:, nodeID].max()
    print(f"Max pressure at node ", nodeID, " is ", maxp, " m")

# plot pressure time series for all the nodes with legend nodeid
results.node["pressure"].plot(legend=True, figsize=(10,6))
plt.ylabel("Pressure (m)")
plt.xlabel("Time (hours)")
plt.show()
