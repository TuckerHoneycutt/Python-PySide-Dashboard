"""
This script will be used for all Volume Conversions as the 
base of the ASCEND tool.
"""

import pandas as pd

def convertSeries(s):
    s = pd.Series(s)
    s = s.apply(float)
    
    return s
    
def Litre2Millilitre(l):
    l = convertSeries(l)

    ml = l * 1000

    return ml

def Litre2Kilolitre(l):
    l = convertSeries(l)
    
    kl = l / 1000
    
    return kl

def Litre2USGallon(l):
    l = convertSeries(l)
    
    floz = Litre2USUSFluidOunce(l)
    gal = USFluidOunce2USGallon(floz)
    
    return gal
    
def Litre2USPint(l):
    l = convertSeries(l)
    
    floz = Litre2USUSFluidOunce(l)
    pt = USFluidOunce2USPint(floz)

    return pt

def Litre2USUSFluidOunce(l):
    l = convertSeries(l)
    
    floz = l * 33.8140227
    return floz

def Millilitre2Litre(ml):
    ml = convertSeries(ml)
    
    l = ml / 1000

    return l

def Millilitre2Kilolitre(ml):
    ml = convertSeries(ml)
    
    kl = ml / 1000000
    
    return kl

def Millilitre2USGallon(ml):
    ml = convertSeries(ml)
    
    floz = Millilitre2USUSFluidOunce(ml)
    gal = USFluidOunce2USGallon(floz)

    return gal
    
def Millilitre2USPint(ml):
    ml = convertSeries(ml)
    
    floz = Millilitre2USUSFluidOunce(ml)
    pt = USFluidOunce2USPint(floz)
    
    return pt

def Millilitre2USUSFluidOunce(ml):
    ml = convertSeries(ml)
    
    l = Millilitre2Litre(ml)
    floz = Litre2USUSFluidOunce(l)

    return floz

def Kilolitre2Litre(kl):
    kl = convertSeries(kl)
    
    l = kl * 1000

    return l

def Kilolitre2Millilitre(kl):
    kl = convertSeries(kl)
    
    kl = kl * 1000000
    
    return kl

def Kilolitre2USGallon(kl):
    kl = convertSeries(kl)
    
    l = Kilolitre2Litre(kl)
    floz = Litre2USUSFluidOunce(l)
    gal = USFluidOunce2USGallon(floz)

    return gal
    
def Kilolitre2USPint(kl):
    kl = convertSeries(kl)
    
    l = Kilolitre2Litre(kl)
    floz = Litre2USUSFluidOunce(l)
    pt = USFluidOunce2USPint(floz)

    return pt

def Kilolitre2USUSFluidOunce(kl):
    kl = convertSeries(kl)
    
    l = Kilolitre2Litre(kl)
    floz = Litre2USUSFluidOunce(l)

    return floz

def USGallon2Litre(gal):
    gal = convertSeries(gal)
    
    floz = USGallon2USUSFluidOunce(gal)
    l = USFluidOunce2Litre(floz)
    
    return l

def USGallon2Millilitre(gal):
    gal = convertSeries(gal)
    
    floz = USGallon2USUSFluidOunce(gal)
    l = USFluidOunce2Litre(floz)
    ml = Litre2Millilitre(l)
    
    return ml

def USGallon2Kilolitre(gal):
    gal = convertSeries(gal)
    
    floz = USGallon2USUSFluidOunce(gal)
    l = USFluidOunce2Litre(floz)
    kl = Litre2Kilolitre(l)
    
    return kl
    
def USGallon2USPint(gal):
    gal = convertSeries(gal)
    
    floz = USGallon2USUSFluidOunce(gal)
    pt = USFluidOunce2USPint(floz)

    return pt

def USGallon2USUSFluidOunce(gal):
    gal = convertSeries(gal)
    
    floz = gal * 128
    
    return floz

def USPint2Litre(pt):
    pt = convertSeries(pt)
    
    floz = USPint2USUSFluidOunce(pt)
    l = USFluidOunce2Litre(floz)

    return l

def USPint2Millilitre(pt):
    pt = convertSeries(pt)
    
    floz = USPint2USUSFluidOunce(pt)
    l = USFluidOunce2Litre(floz)
    ml = Litre2Millilitre(l)
    
    return ml

def USPint2Kilolitre(pt):
    pt = convertSeries(pt)
    
    floz = USPint2USUSFluidOunce(pt)
    l = USFluidOunce2Litre(floz)
    kl = Litre2Kilolitre(l)
    
    return kl
    
def USPint2USGallon(pt):
    pt = convertSeries(pt)
    
    floz = USPint2USUSFluidOunce(pt)
    gal = USFluidOunce2USGallon(floz)
    
    return gal

def USPint2USUSFluidOunce(pt):
    pt = convertSeries(pt)
    
    floz = pt * 16
    
    return floz

def USFluidOunce2Litre(floz):
    floz = convertSeries(floz)
    
    l = floz * 0.02957353

    return l

def USFluidOunce2Millilitre(floz):
    floz = convertSeries(floz)
    
    l = USFluidOunce2Litre(floz)
    ml = Litre2Millilitre(l)
    
    return ml

def USFluidOunce2Kilolitre(floz):
    floz = convertSeries(floz)
    
    l = USFluidOunce2Litre(floz)
    kl = Litre2Kilolitre(l)
    
    return kl
    
def USFluidOunce2USGallon(floz):
    floz = convertSeries(floz)
    
    gal = floz / 128

    return gal

def USFluidOunce2USPint(floz):
    floz = convertSeries(floz)
    
    pt = floz / 16
    
    return pt