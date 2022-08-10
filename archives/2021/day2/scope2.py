# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:22:56 2021

@author: apa
"""


flag=32

def myFunc(number):
    flag=55
    print("From function", number, flag)
    

myFunc(3)
print("From outside", flag)