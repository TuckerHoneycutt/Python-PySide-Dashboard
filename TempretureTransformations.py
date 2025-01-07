"""
This script will be used for all Tempeture Conversions as the 
base of the ASCEND tool.
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