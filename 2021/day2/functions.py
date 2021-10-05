# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:05:49 2021

@author: apa
"""

def greet(name, city, title="Mrs.", grt="Good Morning!"):
    print("Hello", title, name, " from ", city, ".", grt )
    
    
greet("Jane", "Delft")
greet("John", "London", title="Mr.")
greet("Eyre", "Liverpool", grt="Good day")