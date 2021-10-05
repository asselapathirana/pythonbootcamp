# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 08:58:15 2021

@author: apa
"""

# prime number

for num in range(2,10):
    #print("Testing", num)
    prime=True
    for div in range(num-1,1,-1):
      if num%div==0:
          prime=False
          break
    if prime==True: 
        print("Prime: ", num)
    else:
        print("Not prime: ", num)
    