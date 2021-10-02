# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:42:20 2019


@author: nba002
"""
import math

with open("Data1.txt") as file:
    txt=file.read()

#print (txt)
lines=txt.splitlines()
lines=lines[1:]
#print (lines)
for line in lines:
    
    line=line.strip()
   # print(line)
    vals=line.split(",")
    a=float(vals[0])
    b=float(vals[1])
    c=float(vals[2])
   # print(a,b,c)
    arc=b*b-4*a*c
    if(arc<0):
        print("no right solution")
    else:
        x1=(-b+math.sqrt(arc))/(2*a)
        x2=(-b-math.sqrt(arc))/(2*a)
        print("a=",a,"b=",b,"c=",c)
        print("x1=",x1)
        print("x2=",x2)
    
 
    
