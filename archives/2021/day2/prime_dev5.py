# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 09:40:28 2021

@author: apa
"""

from numUtils import isPrime


ct=1
while True:
    if isPrime(ct):
        print(ct)
    ct+=1
    