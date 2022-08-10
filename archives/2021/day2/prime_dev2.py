# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 08:58:15 2021

@author: apa
"""

def isPrime(number):
    # check if num is prime
    prime=True
    for div in range(number-1,1,-1):
      if number%div==0:
          prime=False
          break
    # if prime is True then num is a prime
    return prime


# prime number

for num in range(2,100):
    #print("Testing", num)
    good = isPrime(num)
  
    if good==True: 
        print("Prime: ", num)
    