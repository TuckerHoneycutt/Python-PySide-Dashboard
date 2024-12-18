# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 21:44:20 2024

@author: kayla.green
"""

Position_dict = {
    '': [],
    'ECEF': ["ECEF X", "ECEF Y", "ECEF Z"],
    "UTM": ["Zone","Easting","Northing"],
    "LLA":["Lattitude","Longitude","Altitude"],
    "ENU":["East","North","Up"],
    "NED":["North","East","Down"],
    "LUF":["Left","Up","Forward"],
    "XYZ":["X","Y","Z"],
    "REA":["Range","Elevation","Angle"],
    "RUV":["Ranve","U","V"]
}

PosFrame_dict = {
    '': "",
    'ECEF': "Universal",
    "UTM": "Universal",
    "LLA":"Universal",
    "ENU":"Local",
    "NED":"Local",
    "LUF":"Local",
    "XYZ":"Local",
    "REA":"Local",
    "RUV":"Local"
}

Time_dict = {
    '': [],
    'EPOCH': ["EPOCH"],
    'GPS':['GPS'],
    "TOD": ["Year","JD","TOD ZULU"],
    "SSM":["Year","JD","SSM"],
    "MCI":["Year","JD","MCI", "Ref TOD", "Ref MCI"]
}

TimeFrame_dict = {
    '': "",
    'EPOCH': "Universal",
    "GPS": "Universal",
    "TOD":"Universal",
    "SSM":"Universal",
    "MCI":"Local"
}

Date_dict = {  
    '': [],
    "JD":["Year","JD"],
    "Date":["Year","Month","Day"],
    "Date_String":["Date_String"]
}

#Could be a better way to handle the headers and type
d = {'a1': {'b1': 1, 'b2': 2}, 'a2': {'b1': 3, 'b2': 4}}