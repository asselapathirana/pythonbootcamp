from swmm.toolkit.shared_enum import NodeAttribute
import pyswmm as ps
sim = ps.Simulation('./swmm5Example.inp')
sim.execute()

with ps.Simulation('./swmm5Example.inp') as sim:
    nodes_object = ps.Nodes(sim)
    print([x.nodeid for x in list(nodes_object)])
with ps.Output('./swmm5Example.out') as out:
    print (out.nodes)
    ts = out.node_series('J1', NodeAttribute.INVERT_DEPTH, 0, 55 )
    for index in ts:
        print(index, ts[index])