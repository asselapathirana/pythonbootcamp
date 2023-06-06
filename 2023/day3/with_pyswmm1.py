import pyswmm as ps
sim = ps.Simulation('./data/swmm5Example.inp')
sim.execute()

with ps.Simulation('./data/swmm5Example.inp') as sim:
    nodes_object = ps.Nodes(sim)
    print([x.nodeid for x in list(nodes_object)])
with ps.Output('./data/swmm5Example.out') as out:
    print (out.nodes)
    ts = out.node_series('J1', 'INVERT_DEPTH', 0, 55 )
    for index in ts:
        print(index, ts[index])