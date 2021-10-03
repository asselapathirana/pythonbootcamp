import matplotlib # we need matplotlib for plotting later
matplotlib.use('Qt5Agg') # Not esential. But QtAgg backend seems to work better for plotting
import matplotlib.pyplot as plt # for plotting later

from swmm5.swmm5tools import SWMM5Simulation

st=SWMM5Simulation("small_case.inp")
print("Version = ",st.SWMM5_Version())
print("Number of nodes = ", st.SWMM_Nnodes)
# get the flow in conduit LO3
flow=st.Results("LINK","LO3", 0 ) # 0 is the code for flow in a link (see docs: https://pypi.org/project/SWMM5/
flow=list(flow) # convert the results to a list.
# calculate time list
time=[st.SWMM_ReportStep*x/3600. for x in range(st.SWMM_Nperiods)]
plt.plot(time,flow, 'r', marker="^", label="LO3") # flow hydrograph 
plt.plot(time,list(st.Results("LINK","LO2", 0 )), 'b', marker="*", label="LO2") # another flow hydrograph 
ax = plt.plot(time,list(st.Results("LINK","LO1", 0 )), 'g', marker="d", label="LO1") # another flow hydrograph 
plt.xlabel("Time (h)") # set axes labels
plt.ylabel("Flow (m$^3$/s)")
plt.legend()
plt.show() # show the plot. 