# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:31:50 2021

@author: apa
"""
# I want to check if a number is a prime

def isPrime(number):
    # I have number. 
    # I will check if number can be integer divided by number-1, number-2 ..., 2
    for tn in range(number-1,2,-1):
        if number % tn == 0:
            return False
    return True

ct=1
while True:
    if isPrime(ct):
        print(ct)
    ct+=1
    