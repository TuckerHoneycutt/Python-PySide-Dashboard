"""
Length - Meter, Kilometer, Centimeter, Millimeter, Feet, Yard, Inch, Mile

This script will be used for all Length Conversions as the 
base of the ASCEND tool.
"""

import pandas as pd

def convertSeries(s):
    s = pd.Series(s)
    s = s.apply(float)
    
    return s
    
def Meter2Kilometer(m):
    m = convertSeries(m)

    Km = m / 1000

    return Km

def Meter2Centimeter(m):
    m = convertSeries(m)

    cm = m * 100

    return cm

def Meter2Millimeter(m):
    m = convertSeries(m)

    mm = m * 1000

    return mm

def Meter2Feet(m):
    m = convertSeries(m)
    ft = m * 3.28084
    
    return ft

def Meter2Yard(m):
    m = convertSeries(m)
    yd = m * 1.09361
    
    return yd

def Meter2Inch(m):
    m = convertSeries(m)
    inch = m * 39.3701
    
    return inch

def Meter2Mile(m):
    m = convertSeries(m)
    mile = m * 0.000621371
    
    return mile

def Kilometer2Meter(Km):
    Km = convertSeries(Km)

    m = Km * 1000

    return m

def Kilometer2Centimeter(Km):
    Km = convertSeries(Km)

    cm = Km * 100000

    return cm

def Kilometer2Millimeter(Km):
    Km = convertSeries(Km)

    mm = Km * 1000000

    return mm

def Kilometer2Feet(Km):
    Km = convertSeries(Km)

    m = Kilometer2Meter(Km)
    ft = Meter2Feet(m)
    
    return ft

def Kilometer2Yard(Km):
    Km = convertSeries(Km)

    m = Kilometer2Meter(Km)
    yd = Meter2Yard(m)
    
    return yd

def Kilometer2Inch(Km):
    Km = convertSeries(Km)
    m = Kilometer2Meter(Km)   
    inch = Meter2Inch(m)
    
    return inch

def Kilometer2Mile(Km):
    Km = convertSeries(Km)
    m = Kilometer2Meter(Km)   
    mile = Meter2Mile(m)
    
    return mile

def Centimeter2Meter(cm):
    cm = convertSeries(cm)

    m = cm / 100

    return m

def Centimeter2Kilometer(cm):
    cm = convertSeries(cm)

    Km = cm / 100000

    return Km

def Centimeter2Millimeter(cm):
    cm = convertSeries(cm)

    mm = cm * 1000

    return mm

def Centimeter2Feet(cm):
    cm = convertSeries(cm)
    m = Centimeter2Meter(cm)   
    ft = Meter2Feet(m)
    
    return ft

def Centimeter2Yard(cm):
    cm = convertSeries(cm)
    m = Centimeter2Meter(cm)   
    yd = Meter2Yard(m)
    
    return yd

def Centimeter2Inch(cm):
    cm = convertSeries(cm)
    m = Centimeter2Meter(cm)   
    inch = Meter2Inch(m)
    
    return inch

def Centimeter2Mile(cm):
    cm = convertSeries(cm)
    m = Centimeter2Meter(cm)   
    mile = Meter2Mile(m)
    
    return mile

def Millimeter2Meter(mm):
    mm = convertSeries(mm)

    m = mm / 1000

    return m

def Millimeter2Kilometer(mm):
    mm = convertSeries(mm)

    Km = mm / 100000

    return Km

def Millimeter2Centimeter(mm):
    mm = convertSeries(mm)

    cm = mm * 10

    return cm

def Millimeter2Feet(mm):
    mm = convertSeries(mm)
    m = Millimeter2Meter(mm)   
    ft = Meter2Feet(m)
    
    return ft

def Millimeter2Yard(mm):
    mm = convertSeries(mm)
    m = Millimeter2Meter(mm)   
    yd = Meter2Yard(m)
    
    return yd

def Millimeter2Inch(mm):
    mm = convertSeries(mm)
    m = Millimeter2Meter(mm)   
    inch = Meter2Inch(m)
    
    return inch

def Millimeter2Mile(mm):
    mm = convertSeries(mm)
    m = Millimeter2Meter(mm)   
    mile = Meter2Mile(m)
    
    return mile

def Feet2Meter(ft):
    ft = convertSeries(ft)
    m = ft / 3.28084

    return m

def Feet2Kilometer(ft):
    ft = convertSeries(ft)

    Km = ft * 0.0003048

    return Km

def Feet2Centimeter(ft):
    ft = convertSeries(ft)
    Km = Feet2Kilometer(ft)
    cm = Kilometer2Centimeter(Km)

    return cm

def Feet2Millimeter(ft):
    ft = convertSeries(ft)
    Km = Feet2Kilometer(ft)
    mm = Kilometer2Millimeter(Km)
    
    return mm

def Feet2Yard(ft):
    ft = convertSeries(ft)
    yd = ft / 3

    return yd

def Feet2Inch(ft):
    ft = convertSeries(ft)
    inch = ft * 12
    
    return inch

def Feet2Mile(ft):
    ft = convertSeries(ft)
    mile = ft  / 5280
    
    return mile

def Yard2Meter(yd):
    yd = convertSeries(yd)
    m = yd / 1.09361

    return m

def Yard2Kilometer(yd):
    yd = convertSeries(yd)
    m = Yard2Meter(yd)
    Km = Meter2Kilometer(m)

    return Km

def Yard2Centimeter(yd):
    yd = convertSeries(yd)
    m = Yard2Meter(yd)
    cm = Meter2Centimeter(m)

    return cm

def Yard2Millimeter(yd):
    yd = convertSeries(yd)
    m = Yard2Meter(yd)
    mm = Meter2Millimeter(m)
    
    return mm

def Yard2Feet(yd):
    yd = convertSeries(yd)
    m = Yard2Meter(yd)
    ft = Meter2Feet(m)
    
    return ft

def Yard2Inch(yd):
    yd = convertSeries(yd)
    m = Yard2Meter(yd)
    inch = Meter2Inch(m)
    
    return inch

def Yard2Mile(yd):
    yd = convertSeries(yd)
    m = Yard2Meter(yd)
    mile = Meter2Mile(m)
    
    return mile

def Inch2Meter(inch):
    inch = convertSeries(inch)
    m = inch * 0.0254
    
    return m

def Inch2Kilometer(inch):
    inch = convertSeries(inch)
    m = Inch2Meter(inch)   
    Km = Meter2Kilometer(m)

    return Km

def Inch2Centimeter(inch):
    inch = convertSeries(inch)
    m = Inch2Meter(inch)   
    cm = Meter2Centimeter(m)

    return cm

def Inch2Millimeter(inch):
    inch = convertSeries(inch)
    m = Inch2Meter(inch)   
    mm = Meter2Millimeter(m)

    return mm

def Inch2Feet(inch):
    inch = convertSeries(inch)
    ft = inch / 12   
  
    return ft

def Inch2Yard(inch):
    inch = convertSeries(inch)
    yd = inch / 36
    
    return yd

def Inch2Mile(inch):
    inch = convertSeries(inch)
    mile = inch / 63360
    
    return mile

def Mile2Meter(mile):
    mile = convertSeries(mile)
    m = mile * 1609.34

    return m

def Mile2Kilometer(mile):
    mile = convertSeries(mile)
    m = Mile2Meter(mile)
    Km = Meter2Kilometer(m)

    return Km

def Mile2Centimeter(mile):
    mile = convertSeries(mile)
    m = Mile2Meter(mile)
    cm = Meter2Centimeter(m)

    return cm

def Mile2Millimeter(mile):
    mile = convertSeries(mile)
    m = Mile2Meter(mile)
    mm = Meter2Millimeter(m)
    
    return mm

def Mile2Feet(mile):
    mile = convertSeries(mile)
    ft = mile * 5280
    
    return ft

def Mile2Yard(mile):
    mile = convertSeries(mile)
    yd = mile * 1760
    
    return yd

def Mile2Inch(mile):
    mile = convertSeries(mile)
    inch = mile * 63360
    
    return inch