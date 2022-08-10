import numpy as np
import matplotlib # we need matplotlib for plotting later
matplotlib.use('Qt5Agg') # Not esential. But QtAgg backend seems to work better for plotting
import matplotlib.pyplot as plt # for plotting later

from swmm5.swmm5tools import SWMM5Simulation
from string import Template


area2=75
area3=90
maxfs=[]

for area1 in range(0,100,5):
    with open("small_case.template", 'r') as inf:
        with open("trial.inp", 'w') as outf:
            ins=inf.read()
            ins=Template(ins)
            outs=ins.substitute(a1=area1, a2=area2, a3=area3)
            outf.write(outs)
    #now run
    st=SWMM5Simulation("trial.inp")
    maxf=max(st.Results('NODE','N1', 4))
    print (maxf)
    maxfs.append(maxf)
    ggplot( aesthetics= aes(x = 'weight', y = 'hindfoot_length'), data = surveys_complete)

plt.plot()

