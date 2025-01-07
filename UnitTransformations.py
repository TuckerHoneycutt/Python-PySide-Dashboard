# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:50:06 2025

@author: kayla.green
"""
"""
Length	Meter, Kilometer, Centimeter, Millimeter, Feet, Yard, Inch, Mile
Mass	Gram, Milligram, Kilogram, Ounce, Pound, Ton
Volume	Litre, Millilitre, Kilolitre, Gallon, Pint, Fluid Ounce
Time	Second, Minute, Hour, Day, Month, Week, Year
Temperature	Kelvin, Celsius, Fahrenheit, 
"""

import pandas as pd

def Celsius2Kelvin(C):
    C = pd.Series(C)
    C = C.apply(float)
    
    K = C + 273.15

    return K

def Celsius2Fahrenheit(C):
    C = pd.Series(C)
    C = C.apply(float)
    
    F = ((C/5)*9) + 32
    
    return F

def Kelvin2Celsius(K):
    K = pd.Series(K)
    K = K.apply(float)
    
    C = K - 273.15
    
    return C
    
def Kelvin2Fahrenheit(K):
    K = pd.Series(K)
    K = K.apply(float)
    
    F = (((K - 273.15) / 5)*9) + 32
    
    return F

def Fahrenheit2Celsius(F):
    F = pd.Series(F)
    F = F.apply(float)
    
    C = ((F - 32) / 9)*5
    
    return C

def Fahrenheit2Kelvin(F):
    F = pd.Series(F)
    F = F.apply(float)
    
    K = (((F - 32) / 9)*5) + 273.15
    
    return K