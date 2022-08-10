# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:15:09 2021

@author: apa
"""
# templating example

from string import Template
from swmm5.swmm5tools import SWMM5Simulation
from matplotlib import pyplot as plt


def replace_and_run(values):
    # Open the template file
    with open("small_case.template", "r") as inf:
        txt=inf.read()
    # replace template variable
    result=Template(txt).substitute(a1imp=value)
    #write the result to a INP file
    with open("case.inp", "w") as ouf: 
        ouf.write(result)
    res=SWMM5Simulation("case.inp")
    maxfl=max(list(res.Results('NODE','N1', 4)))
    return maxfl

if __name__=="__main__":
    results=[]
    values=list(range(0,101,5))
    for imp in values:
        ret=replace_and_run(imp)
        results.append(ret)
        print("Ret is : ", ret)
    plt.plot(values, results)
        