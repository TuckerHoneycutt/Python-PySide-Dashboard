# -*- coding: utf-8 -*-
"""
Spyder Editor

This script will be used for all Coordanate Conversion as the 
base of the ASCEND tool.

All outputs are in meters.
"""

import numpy as np
import math
import pandas as pd

a = 6378137.0  # semi-major axis in meters
e2 = 0.00669437999014  # Square of eccentricity
k0 = 0.9996  # Scale factor
e_prime_sq = e2 / (1 - e2)

a_sq=a**2
e = 8.181919084261345e-2


###############################################################################
#ECEF Functions
###############################################################################

#ecef2utm - Good 
def ecef2utm(ecef_x, ecef_y, ecef_z):  
                                   #ecef2lla - Good
    latitude, longitude, altitude = ecef2lla(ecef_x, ecef_y, ecef_z)    
    
    #lla2utm - Good
    return lla2utm(latitude, longitude, altitude)

def ecef2lla(ecef_x, ecef_y, ecef_z, returnUnits = 'LLA_deg'): 
    # x, y and z are in meters
    
    #Constants
    a_sq=a**2
    e = 8.181919084261345e-2
    
    ecefdf = pd.DataFrame()
    
    ecefdf['ecef_x'] = pd.Series(ecef_x)
    ecefdf['ecef_y'] = pd.Series(ecef_y)
    ecefdf['ecef_z'] = pd.Series(ecef_z)
    
    ecefdf['p'] = (ecefdf['ecef_x']**2 + ecefdf['ecef_y']**2)/a_sq
    ecefdf['q'] = ((1 - e2)*(ecefdf['ecef_z']**2))/a_sq
    ecefdf['r'] = (ecefdf['p'] + ecefdf['q'] - e2**2)/6

    ecefdf['evolute'] = 8*ecefdf['r']**3 + ecefdf['p']*ecefdf['q']*(e2**2)
    ecefdf['u'] = ecefdf['evolute']
    
    temp = ecefdf[ecefdf['evolute'] > 0]
    if temp.empty == False:
        temp['u'] = ecefdf['r'] + 0.5*(np.sqrt(8*ecefdf['r']**3 + temp['p']*ecefdf['q']*e2**2) + np.sqrt(temp['p']*ecefdf['q']*e2**2))**(2/3.) + \
				0.5*(np.sqrt(8*ecefdf['r']**3 + temp['p']*ecefdf['q']*e2**2) - np.sqrt(temp['p']*ecefdf['q']*e2**2))**(2/3.)
    
        ecefdf.loc[temp.index] = temp
    
    temp = ecefdf[ecefdf['evolute'] < 0]
    if temp.empty == False:
        u_term1 = np.sqrt(ecefdf['p']*ecefdf['q']*e2**2)/(np.sqrt(-8*ecefdf['r']**3 - temp['p']*ecefdf['q']*e2**2) + np.sqrt(-8*ecefdf['r']**3))
        u_term2 = (-4*ecefdf['r'])*np.sin((2./3.)*np.arctan(u_term1))
        u_term3 = np.cos(np.pi/6 + (2/3)*np.arctan(u_term1))
        temp['u']       = u_term2*u_term3
        
        ecefdf.loc[temp.index] = temp
        
    v = np.sqrt(ecefdf['u']**2 + ecefdf['q']*e2**2)
    w = e2*(ecefdf['u'] + v - ecefdf['q'])/(2*v)
    k = (ecefdf['u'] + v)/(np.sqrt(w**2 + ecefdf['u'] + v) + w)
    d = k*np.sqrt(ecefdf['ecef_x']**2 + ecefdf['ecef_y']**2)/(k + e2)
    ecefdf['altitude'] = np.sqrt(d**2 + ecefdf['ecef_z']**2)*(k + e2 - 1)/k
    ecefdf['latitude'] = 2.*np.atan(ecefdf['ecef_z']/((np.sqrt(d**2 + ecefdf['ecef_z']**2) + d)))

    temp = ecefdf[ecefdf['q'] == 0]
    temp = temp[temp['p'] <= e2**2]
    if temp.empty == False:
        ecefdf['altitude'] = -(a*np.sqrt(1 - e2)*np.sqrt(e2 - ecefdf['p']))/(e)
        phi1 = 2*np.atan(np.sqrt(e2**2 - ecefdf['p'])/(e*(np.sqrt(e2 - ecefdf['p'])) + np.sqrt(1 - e2)*np.sqrt(ecefdf['p'])))
        phi2 = -phi1
        ecefdf['latitude'] = (phi1, phi2)
    
    ecefdf['Case Num'] = 'Case Num' 
    ecefdf['longitude'] = -1 
    
    ecefdf['Case 1-Var1'] = (np.sqrt(2) - 1)*np.sqrt(ecefdf['ecef_y']**2)
    ecefdf['Case 1-Var2'] = np.sqrt(ecefdf['ecef_x']**2 + ecefdf['ecef_y']**2) + ecefdf['ecef_x']
    ecefdf['Case 2-Var1'] = np.sqrt(ecefdf['ecef_x']**2 + ecefdf['ecef_y']**2) + ecefdf['ecef_y']
    ecefdf['Case 2-Var2'] = (np.sqrt(2) + 1)*np.sqrt(ecefdf['ecef_x']**2)
    ecefdf['Case 3-Var1'] = np.sqrt(ecefdf['ecef_x']**2 + ecefdf['ecef_y']**2) - ecefdf['ecef_y']
    ecefdf['Case 3-Var2'] = (np.sqrt(2) + 1)*np.sqrt(ecefdf['ecef_x']**2)


    casedf =  ecefdf[ecefdf['Case 1-Var1'] < ecefdf['Case 1-Var2']]
    if casedf.empty== False:
        casedf['Case Num'] = 'case1'
        casedf['longitude'] = 2.*np.atan(casedf['ecef_y']/(np.sqrt(casedf['ecef_x']**2 + casedf['ecef_y']**2) + casedf['ecef_x']))
        ecefdf.loc[casedf.index.tolist()] = casedf

    casedf = ecefdf[ecefdf['Case Num'] == 'Case Num']
    if casedf.empty== False:
        casedf =  casedf[casedf['Case 2-Var1'] < casedf['Case 2-Var2']]
        if casedf.empty== False:
            casedf['Case Num'] = 'case2'
            casedf['longitude'] = (-1*np.pi/2) - 2*np.atan(casedf['ecef_x']/(np.sqrt(casedf['ecef_x']**2 + casedf['ecef_y']**2) - casedf['ecef_y']))
            ecefdf.loc[casedf.index.tolist()] = casedf

    casedf = ecefdf[ecefdf['Case Num'] == 'Case Num']
    if casedf.empty== False:
        casedf =  casedf[casedf['Case 3-Var1'] < casedf['Case 3-Var2']]
        if casedf.empty== False:
            casedf['Case Num'] = 'case3'
            casedf['longitude'] = (np.pi/2) - 2*np.atan(casedf['ecef_x']/(np.sqrt(casedf['ecef_x']**2 + casedf['ecef_y']**2) + casedf['ecef_y']))
            ecefdf.loc[casedf.index.tolist()] = casedf

    if returnUnits == 'LLA_deg':
        ecefdf['latitude'] = np.degrees(ecefdf['latitude'])
        ecefdf['longitude'] = np.degrees(ecefdf['longitude'])

    return ecefdf['latitude'], ecefdf['longitude'], ecefdf['altitude']
    
def ecef2enu(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'): 
    #LLA_deg, LLA_rad, LLA_dms, ECEF
    # Convert ECEF to LLA

    ecefdf = pd.DataFrame()
    ecefdf['ecefx'] = pd.Series(ecef_x)
    ecefdf['ecefy'] = pd.Series(ecef_y)
    ecefdf['ecefz'] = pd.Series(ecef_z)
    
    ecefdf['ref1'] = ref1
    ecefdf['ref2'] = ref2
    ecefdf['ref3'] = ref3
    
    if 'LLA' in CoordanateRef:
        x0, y0, z0 = lla2ecef(ecefdf['ref1'], ecefdf['ref2'], ecefdf['ref3'])
        lat0, long0, alt0 = ecefdf['ref1'], ecefdf['ref2'], ecefdf['ref3']
        
        if CoordanateRef == 'LLA_deg':
            lat0 = np.radians(ecefdf['ref1'])
            long0 = np.radians(ecefdf['ref2'])
        else:
            lat0 = ecefdf['ref1']
            long0 = ecefdf['ref2']
            
        alt0 = ecefdf['ref3']

    elif 'ECEF' in CoordanateRef:
        lat0, long0, alt0 = ecef2lla(ecefdf['ref1'], ecefdf['ref2'], ecefdf['ref3'], returnUnits = 'LLA_rad')
        x0, y0, z0 = ecefdf['ref1'], ecefdf['ref2'], ecefdf['ref3']

    sin_lambda = np.sin(lat0)
    cos_lambda = np.cos(lat0)
    sin_phi = np.sin(long0)
    cos_phi = np.cos(long0)
    
    xd = ecefdf['ecefx'] - x0
    yd = ecefdf['ecefy'] - y0
    zd = ecefdf['ecefz'] - z0
    
    east = -sin_phi * xd + cos_phi * yd
    north = -cos_phi * sin_lambda * xd - sin_lambda * sin_phi * yd + cos_lambda * zd
    up = cos_lambda * cos_phi * xd + cos_lambda * sin_phi * yd + sin_lambda * zd

    return east, north, up

def ecef2ned(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    east, north, up = ecef2enu(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    return enu2ned (east, north, up)

def ecef2luf(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    east, north, up = ecef2enu(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    return enu2luf (east, north, up)
 
def ecef2xyz(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    print("need conversion")
    x=0
    y=0
    z=0
    
    return x, y, z
  
def ecef2rea(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = 'LLA_deg', returnUnits = 'deg'):
    east, north, up = ecef2enu(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    return enu2rea (east, north, up, returnUnits = returnUnits)

def ecef2ruv(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    x, y, z = ecef2xyz(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = 'LLA_deg')
    return xyz2ruv (x, y, z)

def utm2ecef(zone_number, hemisphere, easting, northing, altitude):

    latitude, longitude, altitude = utm2lla(zone_number, hemisphere, easting, northing, altitude)
    return lla2ecef(latitude, longitude, altitude)

def utm2lla(zone_number, hemisphere, easting, northing, altitude, returnUnits = 'LLA_deg'): 
    #LLA_deg, LLA_rad, LLA_dms, ECEF
    # Convert ECEF to LLA
    # Constants
    eastingOffset = 500000.0
    northingOffset = 10000000.0
    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    mu_divisor = (a * (1- e2 / 4 - 3 * e2 * e2 / 64 -5 * e2 * e2 * e2 /256))
    VAR1 = (3 * e1 / 2 - 27 * e1 * e1 * e1 /32)
    VAR2 = ( 21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32)
    VAR3 = (151 * e1 * e1 * e1 / 96)
    
    utmdf = pd.DataFrame()
    utmdf['zone'] = pd.Series(zone_number)
    utmdf['hemisphere'] = pd.Series(hemisphere)
    utmdf['easting'] = pd.Series(easting)
    utmdf['northing'] = pd.Series(northing)
    utmdf['altitude'] = pd.Series(altitude)
    
    temp = utmdf[utmdf['hemisphere'] != 'N']
    temp['northing'] = northingOffset - temp['northing']
    utmdf.loc[temp.index] = temp

    utmdf['easting'] = utmdf['easting'] - eastingOffset
    
    utmdf['lonOrigin'] = (utmdf['zone'] - 1) * 6 - 180 + 3 # +3 puts in zone centre
    
    utmdf['M'] = utmdf['northing'] / k0 #This finds the meridional arc
    utmdf['mu'] = utmdf['M'] / mu_divisor

    # Calculates the footprint latitude
    utmdf['phi1Rad'] = utmdf['mu'] +  VAR1 * np.sin(2*utmdf['mu']) + VAR2 * np.sin(4*utmdf['mu']) + VAR3 * np.sin(6*utmdf['mu'])

     # Variables for conversion equations
    N1 = a / np.sqrt( 1 - e2 * np.sin(utmdf['phi1Rad']) *  np.sin(utmdf['phi1Rad']))
    T1 = np.tan(utmdf['phi1Rad']) * np.tan(utmdf['phi1Rad'])
    C1 = e_prime_sq * np.cos(utmdf['phi1Rad']) * np.cos(utmdf['phi1Rad'])
    R1 = a * (1 - e2) / np.pow(1 - e2 * np.sin(utmdf['phi1Rad']) * np.sin(utmdf['phi1Rad']), 1.5)
    D = utmdf['easting'] / (N1 * k0)

    # Calculate latitude, in decimal degrees
    latitude = utmdf['phi1Rad'] - ( N1 * np.tan(utmdf['phi1Rad']) / R1) * (D * D / 2 - (5 + 3 * T1 + 10 * C1 - 4 * C1 * C1 - 9 * e_prime_sq) * D * D * D * D / 24 + (61 + 90 * T1 + 298 * C1 + 45 * T1 * T1 - 252 * e_prime_sq - 3 * C1 * C1) * D * D * D * D * D * D / 720)
    latitude = np.degrees(latitude)
    utmdf['latitude'] = latitude
    
    temp = utmdf[utmdf['latitude'] != 'N']
    temp['latitude'] = -1 * temp['latitude']
    utmdf.loc[temp.index] = temp
    
    # Calculate longitude, in decimal degrees
    longitude = (D - (1 + 2 * T1 + C1) * D * D * D / 6 + (5 - 2 * C1 + 28 * T1 - 3 * C1 * C1 + 8 * e_prime_sq + 24 * T1 * T1) * D * D * D * D * D / 120) / np.cos(utmdf['phi1Rad'])
    longitude = utmdf['lonOrigin'] + np.degrees(longitude)
 
    return latitude, longitude, utmdf['altitude']

def utm2enu(zone_number, hemisphere, easting, northing, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'): 
    #LLA_deg, LLA_rad, LLA_dms, ECEF
                                    #utm2lla - Good
    latitude, longitude, altitude = utm2lla(zone_number, hemisphere, easting, northing, altitude)   
    return lla2enu(latitude, longitude, altitude, ref1, ref2, ref3, CoordanateRef = CoordanateRef)

def utm2ned(zone_number, hemisphere, easting, northing, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
                                    #utm2lla - Good
    latitude, longitude, altitude = utm2lla(zone_number, hemisphere, easting, northing, altitude)
    return lla2ned(latitude, longitude, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg')

def utm2luf(zone_number, hemisphere, easting, northing, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
                                    #utm2lla - Good
    latitude, longitude, altitude = utm2lla(zone_number, hemisphere, easting, northing, altitude)
    return lla2luf(latitude, longitude, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg')
 
def utm2xyz(zone_number, hemisphere, easting, northing, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
                                    #utm2lla - Good
    latitude, longitude, altitude = utm2lla(zone_number, hemisphere, easting, northing, altitude)
    return lla2xyz(latitude, longitude, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg')
  
def utm2rea(zone_number, hemisphere, easting, northing, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg', returnUnits = 'deg'):
                                    #utm2lla - Good
    east, north, up = utm2enu(zone_number, hemisphere, easting, northing, altitude, ref1, ref2, ref3)
    return enu2rea(east, north, up, returnUnits = returnUnits)

def utm2ruv(zone_number, hemisphere, easting, northing, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
                                    #utm2lla - Good
    latitude, longitude, altitude = utm2lla(zone_number, hemisphere, easting, northing, altitude)
    return lla2ruv(latitude, longitude, altitude, ref1, ref2, ref3, CoordanateRef = 'LLA_deg')

def lla2ecef(latitude, longitude, altitude, units = 'LLA_deg'): 
    #LLA_deg, LLA_rad, LLA_dms, ECEF
    # Convert ECEF to LLA
    # (lat, lon) in WSG-84 degrees
    # altitude in meters
    
    latitude = pd.Series(latitude)
    longitude = pd.Series(longitude)
    altitude = pd.Series(altitude)
    
    if 'deg' in units:
        latitude = np.radians(latitude)
        longitude = np.radians(longitude)
        
    sin_lat = np.sin(latitude)
    cos_lat = np.cos(latitude)
    sin_lon = np.sin(longitude)
    cos_lon = np.cos(longitude)   

    N = a / np.sqrt(1 - e2 * sin_lat**2)

    ecef_x = (N + altitude) * cos_lat * cos_lon
    ecef_y = (N + altitude) * cos_lat * sin_lon
    ecef_z = ((1 - e2) * N + altitude) * sin_lat
 
    return  ecef_x, ecef_y, ecef_z

def lla2utm(latitude, longitude, altitude, units = 'LLA_deg'): 
    #LLA_deg, LLA_rad, LLA_dms, ECEF
    # Convert ECEF to LLA

    lladf = pd.DataFrame()
    
    lladf['latitude'] = pd.Series(latitude)
    lladf['longitude'] = pd.Series(longitude)
    lladf['altitude'] = pd.Series(altitude)
    
    # Calculate the zone number
    lladf['zone_number'] = (lladf['longitude'] + 180) / 6
    lladf['zone_number'] = lladf['zone_number'].apply(int) + 1

    # Calculate central meridian of the zone
    lladf['lon_origin'] = (lladf['zone_number'] - 1) * 6 - 180 + 3

    if units == 'LLA_deg':
        # Convert latitude and longitude to radians
        lladf['latitude'] = np.radians(lladf['latitude'])
        lladf['longitude'] = np.radians(lladf['longitude'])

    # Calculate the UTM coordinates
    n = a / np.sqrt(1 - e2 * np.sin(lladf['latitude'])**2)
    t = np.tan(lladf['latitude'])**2
    c = e_prime_sq * np.cos(lladf['latitude'])**2
    a1 = np.cos(lladf['latitude']) * (lladf['longitude'] - np.radians(lladf['lon_origin']))

    m = a * ((1 - e2 / 4 - 3 * e2**2 / 64 - 5 * e2**3 / 256) * lladf['latitude'] -
              (3 * e2 / 8 + 3 * e2**2 / 32 + 45 * e2**3 / 1024) * np.sin(2 * lladf['latitude']) +
              (15 * e2**2 / 256 + 45 * e2**3 / 1024) * np.sin(4 * lladf['latitude']) -
              (35 * e2**3 / 3072) * np.sin(6 * lladf['latitude']))

    lladf['easting'] = k0 * n * (a1 + (1 - t + c) * a1**3 / 6 + (5 - 18 * t + t**2 + 72 * c - 58 * e_prime_sq) * a1**5 / 120) + 500000
    lladf['northing'] = k0 * (m + n * np.tan(lladf['latitude']) * (a1**2 / 2 + (5 - t + 9 * c + 4 * c**2) * a1**4 / 24 + (61 - 58 * t + t**2 + 600 * c - 330 * e_prime_sq) * a1**6 / 720))

    temp = lladf[lladf['latitude'] < 0]
    temp['northing'] = temp['northing'] + 10000000 # Adjust for southern hemisphere
    lladf.loc[temp.index] = temp

    return  lladf['zone_number'], lladf['easting'], lladf['northing'], lladf['altitude']
       
def lla2enu(latitude, longitude, altitude, ref1, ref2, ref3, units = 'LLA_deg', CoordanateRef = 'LLA_deg'):

    ecef_x, ecef_y, ecef_z = lla2ecef(latitude, longitude, altitude, units = units)
    return ecef2enu(ecef_x, ecef_y, ecef_z, ref1, ref2, ref3, CoordanateRef = CoordanateRef)

def lla2ned(latitude, longitude, altitude, ref1, ref2, ref3, units = 'LLA_deg', CoordanateRef = 'LLA_deg'):
    
    east, north, up = lla2enu(latitude, longitude, altitude, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    return enu2ned(east, north, up)

def lla2luf(latitude, longitude, altitude, ref1, ref2, ref3, units = 'LLA_deg', CoordanateRef = 'LLA_deg'):
    
    east, north, up = lla2enu(latitude, longitude, altitude, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    return enu2luf(east, north, up)

def lla2xyz(latitude, longitude, altitude, ref1, ref2, ref3, ptl, units = 'LLA_deg', CoordanateRef = 'LLA_deg'):
    print("need conversion")
  
def lla2rea(latitude, longitude, altitude, ref1, ref2, ref3, units = 'LLA_deg', CoordanateRef = 'LLA_deg',  returnUnits = 'deg'):
    
    east, north, up = lla2enu(latitude, longitude, altitude, ref1, ref2, ref3, units = units, CoordanateRef = CoordanateRef)
    return enu2rea(east, north, up,  returnUnits = returnUnits)

def lla2ruv(latitude, longitude, altitude, ref1, ref2, ref3, ptl, units = 'LLA_deg', CoordanateRef = 'LLA_deg'):
    
    x, y, z = lla2xyz(latitude, longitude, altitude, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    return enu2ruv(x, y, z)

def convert_single_enu2ecef(east, north, up, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    
    if 'LLA' in CoordanateRef:
        x0, y0, z0 = lla2ecef(ref1, ref2, ref3)
        
        if CoordanateRef == 'LLA_deg':
            lat0 = math.radians(ref1)
            long0 = math.radians(ref2)
        else:
            lat0, long0 = ref1, ref2

        alt0 = ref3
        
    elif 'ECEF' in CoordanateRef:
        lat0, long0, alt0 = ecef2lla(ref1, ref2, ref3, returnUnits = 'LLA_rad')
        x0, y0, z0 = ref1, ref2, ref3
    
    sin_lambda = math.sin(lat0)
    cos_lambda = math.cos(lat0)
    sin_phi = math.sin(long0)
    cos_phi = math.cos(long0)
    
    #print(sin_lambda, cos_lambda, sin_phi, cos_phi)
    # ENU to ECEF conversion matrix
    t = np.array([[-sin_phi, cos_phi, 0],
                  [-sin_lambda * cos_phi, -sin_lambda * sin_phi, cos_lambda],
                  [cos_lambda*cos_phi, cos_lambda*sin_phi, sin_lambda]])
    
    enu = np.array([east, north, up])

    #print(t.T)
    
    # Calculate ECEF coordinates
    ecef = t.T @ enu + np.array([x0, y0, z0])
    
    #print(t.T)
    #print(enu)
    
    print(t.T @ enu)
    
    return ecef[0]



def enu2ecef(east, north, up, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):

    enudf = pd.DataFrame()
    
    enudf['east'] = east
    enudf['north'] = north
    enudf['up'] = up
    
    enudf['ref1'] = ref1
    enudf['ref2'] = ref2
    enudf['ref3'] = ref3
    
    if 'LLA' in CoordanateRef:
        x0, y0, z0 = lla2ecef(enudf['ref1'], enudf['ref2'], enudf['ref3'])
        
        if CoordanateRef == 'LLA_deg':
            lat0 = np.radians(enudf['ref1'])
            long0 = np.radians(enudf['ref2'])
        else:
            lat0, long0 = enudf['ref1'], enudf['ref2']

        alt0 = enudf['ref3']
        
    elif 'ECEF' in CoordanateRef:
        lat0, long0, alt0 = ecef2lla(enudf['ref1'], enudf['ref2'], enudf['ref3'], returnUnits = 'LLA_rad')
        x0, y0, z0 = enudf['ref1'], enudf['ref2'], enudf['ref3']

    
    sin_lat = np.sin(lat0)
    cos_lat = np.cos(lat0)
    sin_long = np.sin(long0)
    cos_long = np.cos(long0)

    ecef_x = -1*sin_lat*east + sin_long * cos_lat*north + cos_long*cos_lat*up + x0
    ecef_y = cos_lat*east + -1*sin_long*sin_lat*north+ -1*cos_long*sin_lat*up + y0
    ecef_z = cos_long*north + -1*sin_long*up + z0
    
    
    return  ecef_x, ecef_y, ecef_z
    
def enu2utm(east, north, up, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    print("enu2ecef")
    ecef_x, ecef_y, ecef_z = enu2ecef(east, north, up, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    return ecef2utm(ecef_x, ecef_y, ecef_z)

def enu2lla(east, north, up, ref1, ref2, ref3, returnUnits = 'LLA_deg', CoordanateRef = 'LLA_deg'):
    print("enu2ecef")
    ecef_x, ecef_y, ecef_z = enu2ecef(east, north, up, ref1, ref2, ref3, CoordanateRef = CoordanateRef)   
    return ecef2lla(ecef_x, ecef_y, ecef_z, returnUnits = returnUnits)
    
def enu2ned(east, north, up):
    east = pd.Series(east)
    north = pd.Series(north)
    up = pd.Series(up)
    
    return north, east, up*-1

def enu2luf(east, north, up):

    left = -east
    forward = north

    return left, up, forward

def enu2xyz(east, north, up, ptl):
    print("need conversion")
    x=0 
    y=0 
    z=0 
    
    return x, y, z

def enu2rea(east, north, up, returnUnits = 'deg'):
    
    east = pd.Series(east)
    north = pd.Series(north)
    up = pd.Series(up)
    
    r = np.hypot(east, north)
    srange = np.hypot(r,up)

    elevation = np.atan2(up,r)
    azimuth = np.atan2(east, north) % 2*np.pi
    
    if 'deg' in returnUnits:
        elevation = np.degrees(elevation)
        azimuth = np.degrees(azimuth)
    
    return  srange, elevation, azimuth


def enu2ruv(east, north, up, ptl):

    x, y, z = enu2xyz(east, north, up)
    return xyz2rea(x, y, z)
  
def ned2ecef(north, east, down, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    s_down = pd.Series(down)
    return enu2ecef(east, north, -1*s_down, ref1, ref2, ref3, CoordanateRef = CoordanateRef)

def ned2utm(north, east, down, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    s_down = pd.Series(down)
    return enu2utm(east, north, -1*s_down, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
        
def ned2lla(north, east, down, ref1, ref2, ref3, returnUnits = 'LLA_deg', CoordanateRef = 'LLA_deg'):
    s_down = pd.Series(down)
    return enu2lla(east, north, -1*s_down, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    
def ned2enu(north, east, down):
    s_down = pd.Series(down)
    return east, north, -1*s_down
    

def ned2luf(north, east, down):

    return enu2luf(east, north, -down)
 
def ned2xyz(north, east, down, ptl):
    
    return enu2xyz(east, north, -down)
  
def ned2rea(north, east, down, returnUnits = 'deg'):
    s_down = pd.Series(down)
    return enu2rea(east, north, -1*s_down, returnUnits = 'deg')

def ned2ruv(north, east, down, ptl):
    
    return enu2ruv(east, north, -down)
    
def luf2ecef(left, up, forward, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    
    east, north, up = luf2enu(left, up, forward) 
    return enu2ecef(east, north, up, ref1, ref2, ref3, CoordanateRef = CoordanateRef)

def luf2utm(left, up, forward, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    
    east, north, up = luf2enu(left, up, forward) 
    return enu2utm(east, north, up, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
        
def luf2lla(left, up, forward, ref1, ref2, ref3, CoordanateRef = 'LLA_deg'):
    
    east, north, up = luf2enu(left, up, forward)
    return enu2utm(east, north, up, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
    
def luf2enu(left, up, forward):

    east = -left
    north = forward

    return east, north, up

def luf2ned(left, up, forward):
    
    east, north, up = luf2enu(left, up, forward)
    return north, east, -up

def luf2xyz(left, up, forward, ptl):
    
    east, north, up = luf2enu(left, up, forward) 
    return enu2xyz(east, north, up, ptl)
    
def luf2rea(left, up, forward):
    
    east, north, up = luf2enu(left, up, forward) 
    return enu2rea(east, north, up)

def luf2ruv(left, up, forward, ptl):
    
    east, north, up = luf2enu(left, up, forward) 
    return enu2ruv(east, north, up, ptl)
    
def xyz2ecef(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):

    east, north, up = xyz2enu(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
    return enu2ecef(east, north, up, ref1, ref2, ref3, CoordanateRef = CoordanateRef)

def xyz2utm(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):

    east, north, up = xyz2enu(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
    return enu2utm(east, north, up, ref1, ref2, ref3, CoordanateRef = CoordanateRef)
        
def xyz2lla(x, y, z, ref1, ref2, ref3, ptl, returnUnits = 'LLA_deg', CoordanateRef = 'LLA_deg'):

    east, north, up = xyz2enu(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
    return enu2lla(east, north, up, ref1, ref2, ref3, returnUnits= returnUnits)
    
def xyz2enu(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):
    print("need conversion")
    east = 0 
    north = 0 
    up = 0 
    return east, north, up

def xyz2ned(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):
    
    east, north, up = xyz2enu(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
    return enu2ned(east, north, up)
 
def xyz2luf(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):
    
    east, north, up = xyz2enu(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
    return enu2luf(east, north, up)
  
def xyz2rea(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):
    
    east, north, up = xyz2enu(x, y, z, ref1, ref2, ref3, ptl)
    return enu2ruv(east, north, up)

def xyz2ruv(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):
    
    print("calculations needed")
    srange = 0
    elevation = 0 
    azimuth = 0
    return srange, elevation, azimuth
    
def rea2ecef(srange, elevation, azimuth, ref1, ref2, ref3, units = 'deg', CoordanateRef = 'LLA_deg'):

    east, north, up = rea2enu(srange, elevation, azimuth, units = units)
    return enu2ecef(east, north, up, ref1, ref2, ref3, CoordanateRef=CoordanateRef)

def rea2utm(srange, elevation, azimuth, ref1, ref2, ref3, units = 'deg', CoordanateRef = 'LLA_deg'):
    
    east, north, up = rea2enu(srange, elevation, azimuth, units = units)
    return enu2utm(east, north, up, ref1, ref2, ref3, CoordanateRef=CoordanateRef)
        
def rea2lla(srange, elevation, azimuth, ref1, ref2, ref3, units = 'deg', CoordanateRef = 'LLA_deg', returnUnits = 'LLA_deg'):
    
    east, north, up = rea2enu(srange, elevation, azimuth, units = units)
    return enu2lla(east, north, up, ref1, ref2, ref3, CoordanateRef=CoordanateRef, returnUnits = returnUnits)
    
def rea2enu(srange, elevation, azimuth, units = 'deg'):

    srange = pd.Series(srange)
    elevation = pd.Series(elevation)
    azimuth = pd.Series(azimuth)
    
    if units == 'deg':
        azimuth = np.radians(azimuth)
        elevation = np.radians(elevation)

    east = srange * np.cos(elevation) * np.sin(azimuth)
    north = srange * np.cos(elevation) * np.cos(azimuth)
    up = srange * np.sin(elevation)
  
    return  east, north, up


def rea2ned(srange, elevation, azimuth, units = 'deg'):
    
    east, north, up = rea2enu(srange, elevation, azimuth, units = units)
    return enu2ned(east, north, up)
    
 
def rea2luf(srange, elevation, azimuth, units = 'deg'):
    
    east, north, up = rea2enu(srange, elevation, azimuth, units = units)
    return enu2luf(east, north, up)
  
def rea2xyz(srange, elevation, azimuth, ref1, ref2, ref3, ptl, units = 'deg', CoordanateRef='LLA_deg'):
    
    east, north, up = rea2enu(srange, elevation, azimuth, units = units)
    return enu2xyz(east, north, up, ref1, ref2, ref3, ptl, CoordanateRef=CoordanateRef)

def rea2ruv(srange, elevation, azimuth, ref1, ref2, ref3, ptl, units = 'deg', CoordanateRef = 'LLA_deg'):
    
    east, north, up = rea2enu(srange, elevation, azimuth, units = units)
    return enu2ruv(east, north, up, ref1, ref2, ref3, ptl, CoordanateRef=CoordanateRef)
    
def ruv2ecef(srange, u, v, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):

    x,y,z = ruv2xyz(srange, u, v)
    return xyz2ecef(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)

def ruv2utm(srange, u, v, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):

    x,y,z = ruv2xyz(srange, u, v)
    return xyz2utm(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
    
def ruv2lla(srange, u, v, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):

    x,y,z = ruv2xyz(srange, u, v)
    return xyz2lla(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
    
def ruv2enu(srange, u, v, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):

    x,y,z = ruv2xyz(srange, u, v)
    return xyz2enu(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)

def ruv2ned(srange, u, v, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):
    
    x,y,z = ruv2xyz(srange, u, v)
    return xyz2ned(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
 
def ruv2luf(srange, u, v, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):

    x,y,z = ruv2xyz(srange, u, v)
    return xyz2luf(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)
  
def ruv2xyz(srange, u, v):
    print("need conversion")
    x=0 
    y=0 
    z=0 
    
    return x, y, z

def ruv2rea(srange, u, v, ref1, ref2, ref3, ptl, CoordanateRef = 'LLA_deg'):

    x,y,z = ruv2xyz(srange, u, v)
    return xyz2rea(x, y, z, ref1, ref2, ref3, ptl, CoordanateRef = CoordanateRef)

def dms_to_decimal_degrees(dms_degrees):
    dms = dms_degrees.split(":")   
    return dms[0] + (dms[1]/60) + (dms[2]/3600)
    
def decimal_degrees_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    remainder = abs(decimal_degrees - int(decimal_degrees))
    minutes = int(remainder * 60)
    seconds = int((remainder * 60 - minutes) * 60)
    return degrees, minutes, seconds

def MasterCoordinatesConvert(InputRef, OutputRef, Input1Var, Input2Var, Input3Var, 
            Input4Var = np.nan, Input5Var = np.nan, ref1 = np.nan, ref2 = np.nan,
            ref3 = np.nan, ref4 = np.nan, units = 'LLA_deg', CoordanateRef = 'LLA_deg', 
            returnUnits = 'LLA_deg'):

    if InputRef == "ECEF": 
        if OutputRef == "UTM":
            res1, res2, res3, res4 = ecef2utm(Input1Var, Input2Var, Input3Var)
            
        elif OutputRef == "LLA":
            res1, res2, res3 = ecef2lla(Input1Var, Input2Var, Input3Var, returnUnits = returnUnits) 

        elif OutputRef == "ENU":
            res1, res2, res3 = ecef2enu(Input1Var, Input2Var, Input3Var, 
                        ref1, ref2, ref3, CoordanateRef = CoordanateRef)  

        elif OutputRef == "NED":
            res1, res2, res3 = ecef2ned(Input1Var, Input2Var, Input3Var, 
                        ref1, ref2, ref3, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LUF":
            res1, res2, res3 = ecef2luf(Input1Var, Input2Var, Input3Var, 
                        ref1, ref2, ref3, CoordanateRef = CoordanateRef) 

        elif OutputRef == "XYZ":
            res1, res2, res3 = ecef2xyz(Input1Var, Input2Var, Input3Var, 
                        ref1, ref2, ref3, CoordanateRef = CoordanateRef)  

        elif OutputRef == "REA":
            res1, res2, res3 = ecef2rea(Input1Var, Input2Var, Input3Var, 
                        ref1, ref2, ref3, CoordanateRef = CoordanateRef, returnUnits = returnUnits)

        elif OutputRef == "RUV":
            res1, res2, res3 = ecef2ruv(Input1Var, Input2Var, Input3Var, 
                        ref1, ref2, ref3, CoordanateRef = CoordanateRef)

    elif InputRef == "UTM":
        if OutputRef == "ECEF":
            res1, res2, res3 = utm2ecef(Input1Var, Input2Var, Input3Var, Input4Var, Input5Var)

        elif OutputRef == "LLA":
            res1, res2, res3 = utm2lla(Input1Var, Input2Var, Input3Var, Input4Var, Input5Var, 
                                       returnUnits = returnUnits)

        elif OutputRef == "ENU":
            res1, res2, res3 = utm2enu(Input1Var, Input2Var, Input3Var, Input4Var, Input5Var, 
                                       ref1, ref2, ref3, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "NED":
            res1, res2, res3 = utm2ned(Input1Var, Input2Var, Input3Var, Input4Var, Input5Var, 
                                       ref1, ref2, ref3, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LUF":
            res1, res2, res3 = utm2luf(Input1Var, Input2Var, Input3Var, Input4Var, Input5Var, 
                                       ref1, ref2, ref3, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "XYZ":
            res1, res2, res3 = utm2xyz(Input1Var, Input2Var, Input3Var, Input4Var, Input5Var, 
                                       ref1, ref2, ref3, CoordanateRef = CoordanateRef) 
            
        elif OutputRef == "REA":
            res1, res2, res3 = utm2rea(Input1Var, Input2Var, Input3Var, Input4Var, Input5Var, 
                                       ref1, ref2, ref3, CoordanateRef = CoordanateRef, 
                                       returnUnits = returnUnits)
            
        elif OutputRef == "RUV":
            res1, res2, res3 = utm2ruv(Input1Var, Input2Var, Input3Var, Input4Var, Input5Var, 
                                       ref1, ref2, ref3, CoordanateRef = CoordanateRef)
        
    elif InputRef == "LLA":
        if OutputRef == "ECEF":
            res1, res2, res3 = lla2ecef(Input1Var, Input2Var, Input3Var, units = units)
            
        elif OutputRef == "UTM":
            res1, res2, res3, res4 = lla2utm(Input1Var, Input2Var, Input3Var, units = units)  
            
        elif OutputRef == "ENU":
            res1, res2, res3 = lla2enu(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       units = units, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "NED":
            res1, res2, res3 = lla2ned(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       units = units, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LUF":
            res1, res2, res3 = lla2luf(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       units = units, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "XYZ":
            res1, res2, res3 = lla2xyz(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       units = units, CoordanateRef = CoordanateRef) 
            
        elif OutputRef == "REA":
            res1, res2, res3 = lla2rea(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       units = units, CoordanateRef = CoordanateRef, 
                                       returnUnits = returnUnits)
            
        elif OutputRef == "RUV":
            res1, res2, res3 = lla2ruv(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       units = units, CoordanateRef = CoordanateRef, 
                                       returnUnits = returnUnits)

    elif InputRef == "ENU":
        if OutputRef == "ECEF":
            res1, res2, res3 = enu2ecef(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                        CoordanateRef = CoordanateRef)
            
        elif OutputRef == "UTM":
            res1, res2, res3, res4 = enu2utm(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LLA":
            res1, res2, res3 = enu2lla(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       CoordanateRef = CoordanateRef, returnUnits = returnUnits) 
            
        elif OutputRef == "NED":
            res1, res2, res3 = enu2ned(Input1Var, Input2Var, Input3Var)  
            
        elif OutputRef == "LUF":
            res1, res2, res3 = enu2luf(Input1Var, Input2Var, Input3Var) 
            
        elif OutputRef == "XYZ":
            res1, res2, res3 = enu2xyz(Input1Var, Input2Var, Input3Var, ref1) 
            
        elif OutputRef == "REA":
            res1, res2, res3 = enu2rea(Input1Var, Input2Var, Input3Var, returnUnits = returnUnits)
            
        elif OutputRef == "RUV":
            res1, res2, res3 = enu2ruv(Input1Var, Input2Var, Input3Var, ref1)
        
    elif InputRef == "NED":
        if OutputRef == "ECEF":
            res1, res2, res3 = ned2ecef(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                        CoordanateRef = CoordanateRef)
            
        elif OutputRef == "UTM":
            res1, res2, res3, res4 = ned2utm(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LLA":
            res1, res2, res3 = ned2lla(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       CoordanateRef = CoordanateRef, returnUnits = returnUnits)  
            
        elif OutputRef == "ENU":
            res1, res2, res3 = ned2enu(Input1Var, Input2Var, Input3Var) 
            
        elif OutputRef == "LUF":
            res1, res2, res3 = ned2luf(Input1Var, Input2Var, Input3Var)  
            
        elif OutputRef == "XYZ":
            res1, res2, res3 = ned2xyz(Input1Var, Input2Var, Input3Var, ref1)  
            
        elif OutputRef == "REA":
            res1, res2, res3 = ned2rea(Input1Var, Input2Var, Input3Var, returnUnits = returnUnits)
            
        elif OutputRef == "RUV":
            res1, res2, res3 = ned2ruv(Input1Var, Input2Var, Input3Var, ref1)
        
    elif InputRef == "LUF":
        if OutputRef == "ECEF":
            res1, res2, res3 = luf2ecef(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                        CoordanateRef = CoordanateRef)
            
        elif OutputRef == "UTM":
            res1, res2, res3, res4, res5 = luf2utm(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LLA":
            res1, res2, res3 = luf2lla(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, 
                                       CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "ENU":
            res1, res2, res3 = luf2enu(Input1Var, Input2Var, Input3Var)  
            
        elif OutputRef == "NED":
            res1, res2, res3 = luf2ned(Input1Var, Input2Var, Input3Var) 
            
        elif OutputRef == "XYZ":
            res1, res2, res3 = luf2xyz(Input1Var, Input2Var, Input3Var, ref1) 
            
        elif OutputRef == "REA":
            res1, res2, res3 = luf2rea(Input1Var, Input2Var, Input3Var)
            
        elif OutputRef == "RUV":
            res1, res2, res3 = luf2ruv(Input1Var, Input2Var, Input3Var, ref1)
        
    elif InputRef == "XYZ":
        if OutputRef == "ECEF":
            res1, res2, res3 = xyz2ecef(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                        CoordanateRef = CoordanateRef)
            
        elif OutputRef == "UTM":
            res1, res2, res3, res4, res5 = xyz2utm(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                        CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LLA":
            res1, res2, res3 = xyz2lla(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       returnUnits = returnUnits, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "ENU":
            res1, res2, res3 = xyz2enu(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "NED":
            res1, res2, res3 = xyz2ned(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef) 
            
        elif OutputRef == "LUF":
            res1, res2, res3 = xyz2luf(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "REA":
            res1, res2, res3 = xyz2rea(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef)
            
        elif OutputRef == "RUV":
            res1, res2, res3 = xyz2ruv(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef)
        
    elif InputRef == "REA":
        if 'deg' in units:
            units = 'deg'
        else:
            units = 'rad'
            
        if OutputRef == "ECEF":
            res1, res2, res3 = rea2ecef(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3,
                                        units = units, CoordanateRef = CoordanateRef)
            
        elif OutputRef == "UTM":
            res1, res2, res3, res4 = rea2utm(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3,
                                        units = units, CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LLA":
            res1, res2, res3 = rea2lla(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3,
                                       units = units, CoordanateRef = CoordanateRef, 
                                       returnUnits = returnUnits)  
            
        elif OutputRef == "ENU":
            res1, res2, res3 = rea2enu(Input1Var, Input2Var, Input3Var, units = units)  
            
        elif OutputRef == "NED":
            res1, res2, res3 = rea2ned(Input1Var, Input2Var, Input3Var, units = units) 
            
        elif OutputRef == "LUF":
            res1, res2, res3 = rea2luf(Input1Var, Input2Var, Input3Var, units = units) 
            
        elif OutputRef == "XYZ":
            res1, res2, res3 = rea2xyz(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       units = units, CoordanateRef = CoordanateRef)
            
        elif OutputRef == "RUV":
            res1, res2, res3 = rea2ruv(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       units = units, CoordanateRef = CoordanateRef)
        
    elif InputRef == "RUV":
        if OutputRef == "ECEF":
            res1, res2, res3 = ruv2ecef(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                        CoordanateRef = CoordanateRef)
            
        elif OutputRef == "UTM":
            res1, res2, res3, res4, res5 = ruv2utm(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef) 
            
        elif OutputRef == "LLA":
            res1, res2, res3 = ruv2lla(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef) 
            
        elif OutputRef == "ENU":
            res1, res2, res3 = ruv2enu(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef) 
            
        elif OutputRef == "NED":
            res1, res2, res3 = ruv2ned(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "LUF":
            res1, res2, res3 = ruv2luf(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef)  
            
        elif OutputRef == "XYZ":
            res1, res2, res3 = ruv2xyz(Input1Var, Input2Var, Input3Var)
            
        elif OutputRef == "REA":
            res1, res2, res3 = ruv2rea(Input1Var, Input2Var, Input3Var, ref1, ref2, ref3, ref4,
                                       CoordanateRef = CoordanateRef)
    
    if OutputRef == "UTM":
        return res1, res2, res3, res4
    else:
        return res1, res2, res3