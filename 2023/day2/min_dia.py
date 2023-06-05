# import wntr   
import wntr

# Create a water network model
inp_file = 'data/Netx.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

# find the diameter of those pipes
diameters = wn.query_link_attribute('diameter')
print(diameters['10'])

# write a function that takes wn and pipe_id as input and returns the minimum pressure
def min_pressure(wn):
    # run a simulation
    sim = wntr.sim.WNTRSimulator(wn)
    results = sim.run_sim()
    # extract the pressure at the junction
    pressure = results.node['pressure']
    # find the minimum pressure
    min_pressure = pressure.min(axis=0)
    # remove the node id '9' from the list
    min_pressure = min_pressure.drop('9')
    #find the minimum pressure in the list
    mp = min_pressure.min()
    return mp

# fuction to change the diameter of pipe '10' to value x
def change_diameter(wn, x):
    # change the diameter of pipe '10' to value x
    wn.get_link('10').diameter = x

dia=diameters['10']
step=0.01
i=0
while True:
    dia=dia-step*i
    change_diameter(wn, dia)
    mp = min_pressure(wn)
    if mp is None:
        print("no solution")
        break
    i=i+1
    print(dia, mp)
    if mp < 20:
        print("minimum diameter is ", dia )
        break