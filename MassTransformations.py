"""
This script will be used for all Mass Conversions as the 
base of the ASCEND tool.
"""

import pandas as pd

def convertSeries(s):
    s = pd.Series(s)
    s = s.apply(float)
    
    return s

def Gram2Milligram(g):
    g = convertSeries(g)

    mg = g * 1000
    
    return mg

def Gram2Kilogram(g):
    g = convertSeries(g)

    Kg = g / 1000
    
    return Kg

def Gram2Ounce(g):
    g = convertSeries(g)
    oz = g * 0.0352739619

    return oz

def Gram2Pound(g):
    g = convertSeries(g)
    lbs = g * 0.00220462

    return lbs

def Gram2Ton(g):
    g = convertSeries(g)
    ton = g / 907,184.74

    return ton


def Milligram2Gram(mg):
    mg = convertSeries(mg)
    
    g = mg / 1000
    
    return g

def Milligram2Kilogram(mg):
    mg = convertSeries(mg)
    
    Kg = mg / 1000000
    
    return Kg

def Milligram2Ounce(mg):
    mg = convertSeries(mg)
    
    g = Milligram2Gram(mg)
    oz = Gram2Ounce(g)
    
    return oz

def Milligram2Pound(mg):
    mg = convertSeries(mg)
    
    g = Milligram2Gram(mg)
    lbs = Gram2Pound(g)
    
    return lbs

def Milligram2Ton(mg):
    mg = convertSeries(mg)
    
    g = Milligram2Gram(mg)
    Ton = Gram2Ton(g)
    
    return Ton

def Kilogram2Gram(Kg):
    Kg = convertSeries(Kg)
    
    g = Kg / 1000
    
    return g

def Kilogram2Milligram(Kg):
    Kg = convertSeries(Kg)
    
    g = Kilogram2Gram(Kg)
    mg = Gram2Milligram(g)
    
    return mg

def Kilogram2Ounce(Kg):
    Kg = convertSeries(Kg)
    
    g = Kilogram2Gram(Kg)
    oz = Gram2Ounce(g)
    
    return oz

def Kilogram2Pound(Kg):
    Kg = convertSeries(Kg)
    
    g = Kilogram2Gram(Kg)
    lbs = Gram2Pound(g)
    
    return lbs

def Kilogram2Ton(Kg):
    Kg = convertSeries(Kg)
    
    g = Kilogram2Gram(Kg)
    Ton = Gram2Ton(g)
    
    return Ton

def Ounce2Gram(oz):
    oz = convertSeries(oz)
    g = oz * 28.3495

    return g

def Ounce2Milligram(oz):
    oz = convertSeries(oz)
    
    g = Ounce2Gram(oz)
    mg = Gram2Milligram(g)
    
    return mg

def Ounce2Kilogram(oz):
    oz = convertSeries(oz)
    
    g = Ounce2Gram(oz)
    Kg = Gram2Kilogram(g)
    
    return Kg

def Ounce2Pound(oz):
    oz = convertSeries(oz)
    lbs = oz / 16

    return lbs

def Ounce2Ton(oz):
    oz = convertSeries(oz)
    Ton = oz / 32,000

    return Ton

def Pound2Gram(lbs):
    lbs = convertSeries(lbs)
    g = lbs * 453.59237

    return g

def Pound2Milligram(lbs):
    lbs = convertSeries(lbs)
    
    g = Pound2Gram(lbs)
    mg = Gram2Milligram(g)
    
    return mg

def Pound2Kilogram(lbs):
    lbs = convertSeries(lbs)
    
    g = Pound2Gram(lbs)
    Kg = Gram2Kilogram(g)
    
    return Kg

def Pound2Ounce(lbs):
    lbs = convertSeries(lbs)
    oz = lbs * 16

    return oz

def Pound2Ton(lbs):
    lbs = convertSeries(lbs)
    
    Ton = lbs / 2000
    
    return Ton

def Ton2Gram(Ton):
    Ton = convertSeries(Ton)
    g = Ton * 907,184.74

    return g

def Ton2Milligram(Ton):
    Ton = convertSeries(Ton)
    
    g = Ton2Gram(Ton)
    mg = Gram2Milligram(g)
    
    return mg

def Ton2Kilogram(Ton):
    Ton = convertSeries(Ton)
    
    g = Ton2Gram(Ton)
    Kg = Gram2Kilogram(g)
    
    return Kg

def Ton2Ounce(Ton):
    Ton = convertSeries(Ton)
    
    lbs = Ton2Pound(Ton)
    oz = Pound2Ounce(lbs)

    return oz

def Ton2Pound(Ton):
    Ton = convertSeries(Ton)
    
    lbs = Ton * 2000

    return lbs