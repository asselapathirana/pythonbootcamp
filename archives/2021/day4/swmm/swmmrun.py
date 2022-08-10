from swmm5.swmm5tools import SWMM5Simulation

st=SWMM5Simulation("small_case.INP")
print("")
print(st.SWMM5_Version())
print(st.Subcatch())