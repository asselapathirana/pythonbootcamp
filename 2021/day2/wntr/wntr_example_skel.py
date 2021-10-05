# Copyright (c) 2021 Assela Pathirana
# 
# This software is released under the MIT License.
# https:#opensource.org/licenses/MIT

"""
The following example demonstrates how to import WNTR, generate a water network 
model from an INP file, simulate hydraulics, and plot simulation results on the network.
"""
import wntr

# Create a water network model
inp_file = 'data/Net3LPS.inp'
wn = wntr.network.WaterNetworkModel(inp_file)
print(wn.describe())
skel_wn = wntr.morph.skeletonize(wn, 48*0.0254)
print(skel_wn.describe())
skel_wn.write_inpfile(inp_file[:-4]+'_skel.inp', version=2.2)
