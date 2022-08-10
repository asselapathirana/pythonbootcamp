# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 10:15:09 2021

@author: apa
"""
# templating example

from string import Template
from swmm5.swmm5tools import SWMM5Simulation
from matplotlib import pyplot as plt


def replace_and_run(v1, v2, v3):
    # Open the template file
    with open("small_case.template2", "r") as inf:
        txt=inf.read()
    # replace template variable
    result=Template(txt).substitute(a1imp=v1, a2imp=v2, a3imp=v3 )
    #write the result to a INP file
    with open("case.inp", "w") as ouf: 
        ouf.write(result)
    res=SWMM5Simulation("case.inp")
    maxfl=max(list(res.Results('NODE','N3', 4)))
    return maxfl

if __name__=="__main__":
    
    values=list(range(0,101,50))
    for impA2 in values:
        results=[]
        for impA1 in values:
            print(impA2, impA1)
            ret=replace_and_run(impA1, impA2, 90)
            results.append(ret)
            print("Ret is : ", ret)
        plt.plot(values, results)
    plt.show()
        