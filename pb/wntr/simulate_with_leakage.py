from matplotlib import pyplot as plt
import wntr
import copy
import pickle

class wntr_leakage:
    
    def __init__(self,inp_filename):

        self.wn = wntr.network.WaterNetworkModel(inp_filename) 
        self.inp_filename=inp_filename
        self.pickle_name = self.inp_filename+".pickle"
            
    
    def add_leaks(self, leak_area_sqm_per_km):
        self.wnl = copy.deepcopy(self.wn)
        self.leakage_nodes = []
        for link_name, link in self.wn.links():
            if link.link_type == "Pipe":
                #print (link_name)
                nl = link_name+"_node"
                self.wnl = wntr.morph.link.split_pipe(self.wnl, link_name, link_name +"_1",  nl)
                self.leakage_nodes.append(nl)
                la = link.length/1000.*leak_area_sqm_per_km  
                #print(link_name, nl, link.length, la)
                self.wnl.get_node(nl).add_leak(self.wnl,la, start_time=0, end_time=None) 
         
 
        self.save()

    def save(self):
        with open(self.pickle_name,'wb') as ff:
            pickle.dump(self.wnl,ff)
       
    def load(self):
        with open(self.pickle_name,'rb') as ff:
            self.wnl = pickle.load(ff)     
        


    def adf_leak(self):
             
        sim = wntr.sim.WNTRSimulator(self.wnl, mode='PDD')
        results = sim.run_sim()
        delivered_demand=results.node['demand'][self.wnl.junction_name_list].sum().sum() # get only the results of junctions - removing tanks, reservoirs etc.
        expected_demand = wntr.metrics.hydraulic.expected_demand(self.wnl)[self.wnl.junction_name_list].sum().sum() 
        leak_demand = results.node['leak_demand'].sum().sum()
        lr = 1- leak_demand/(leak_demand + delivered_demand.sum().sum()) # we return total supply-leakage (1-lr is the leakage then)
        return delivered_demand/expected_demand, lr





if __name__== '__main__':
    
    inpfile='Net3LPS.inp'
    wl=wntr_leakage(inpfile)
    print("1")
    wl.add_leaks(200/1.e6)  # x sq. mm (x/1.e6 sq.m in the equation - remember WNTR users m) for each 1 km of pipe)
    print("2")
    adf_leak = wl.adf_leak()
    print("1",adf_leak)   


    # change system 


    #wl.wnl.get_node('1').elevation, wl.wnl.get_node('2').elevation, wl.wnl.get_node('3').elevation, \
    #    wl.wnl.get_node('River').head, wl.wnl.get_node('Lake').head  = [43, 37, 40, 68,52]
    wl.wnl.get_link('101').diameter, wl.wnl.get_link('60').diameter, wl.wnl.get_link('20').diameter, \
    wl.wnl.get_link('40').diameter, wl.wnl.get_link('50').diameter = [100,100,100,100,100]
    print("2",wl.adf_leak())
    wl.load()
    print("3",wl.adf_leak())  
    wl.load()
    wl.wnl.get_link('101').diameter, wl.wnl.get_link('60').diameter, wl.wnl.get_link('20').diameter, \
    wl.wnl.get_link('40').diameter, wl.wnl.get_link('50').diameter = [150,150,150,150,150]
    print("4",wl.adf_leak())
    wl.load()
    print("5",wl.adf_leak())        
    print("done")