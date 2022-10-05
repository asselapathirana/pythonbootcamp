
from operator import ge
from webbrowser import get
import pyswmm as ps
from swmm.toolkit.shared_enum import LinkAttribute


"""Given inpf - a SWMM input file, and a link index outlink
Run SWMM and return maximum flow at outlink """
def get_max_flow(inpf, ol):
    outfile=inpf[:-4]+".out"
    sim = ps.Simulation(inpf)
    sim.execute()
    with ps.Output(outfile) as out:
        ts = out.link_series(ol, LinkAttribute.FLOW_RATE)
        flows = ts.values()
        maxv = max(flows)
        return maxv


if __name__=="__main__":
    inpdir="./data/"
    inpfile=inpdir+"swmm5Example.inp"
    outlink='T5'
    mv=get_max_flow(inpfile, outlink)
    print(f"The maximum flow in {outlink} is {mv:.2f}")