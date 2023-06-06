import pyswmm as ps
sim = ps.Simulation('./data/swmm5Example.inp')
sim.execute()

with ps.Output('./data/swmm5Example.out') as out:
    print (out.nodes)
    ts1 = out.node_series('J1', 'INVERT_DEPTH', 0, 55 )
    ts2 = out.node_series('J7', 'INVERT_DEPTH', 0, 55 )
    for index in ts1:
        print(index, ts1[index], ts2[index])