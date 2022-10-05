from matplotlib import pyplot as plt
from src import swmm_call as sc
from src import templater as te

TEMPLATEFILE='./data/swmm5Example.inp_'
OUTPUTLINK='T5'

imps=list(range(0,101,10))
maxfs=[]
print(imps)
for imp in imps:
    outputfile=f"./output/TRIAIL_{imp}.inp"
    te.write_inp(TEMPLATEFILE,outputfile, imp)
    maxf=sc.get_max_flow(outputfile,OUTPUTLINK)
    maxfs.append(maxf)

plt.plot(imps, maxfs)
plt.show()