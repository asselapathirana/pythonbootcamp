# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:27:30 2021

@author: apa
"""
# calculate the squre of a series of numbers

numbers = [23, 55, 1024, 100]

sqs=[] # create an empty list
for item in numbers:
    sqs.append(item**2)
    
print(sqs)