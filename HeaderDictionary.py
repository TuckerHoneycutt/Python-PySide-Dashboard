# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 21:44:20 2024

@author: kayla.green
"""
import json

Position_dict = {
    "ECEF": ["ECEF X", "ECEF Y", "ECEF Z"],
    "UTM": ["Zone Number","Zone Letter","Easting","Northing","Altitude"],
    "LLA":["Lattitude","Longitude","Altitude"],
    "ENU":["East","North","Up"],
    "NED":["North","East","Down"],
    "LUF":["Left","Up","Forward"],
    "XYZ":["X","Y","Z"],
    "REA":["Range","Elevation","Angle"],
    "RUV":["Slantrange","U","V"]
}

PosFrame_dict = {
    "ECEF": "Universal",
    "UTM": "Universal",
    "LLA":"Universal",
    "ENU":"Local",
    "NED":"Local",
    "LUF":"Local",
    "XYZ":"Local",
    "REA":"Local",
    "RUV":"Local"
}

def UpdateHeaders(file, user_data, key, value):
    if key in user_data.keys():
        values = user_data[key]
        user_data[key] = values + [value] 
    else:
        user_data[key] = [value]
    
    # Save updated data to file
    with open(file, 'w') as file:
        json.dump(user_data, file)
    
    return user_data

Time_dict = {
    'EPOCH': ["Seconds", "Nanoseconds"],
    'GPS':["Seconds", "Nanoseconds"],
    "TOD": ["Year","JD","TOD ZULU"],
    "SSM":["Year","JD","SSM"],
    "MCI":["Year","JD","MCI", "Ref TOD", "Ref MCI"]
}

TimeFrame_dict = {
    'EPOCH': "Universal",
    "GPS": "Universal",
    "TOD":"Universal",
    "SSM":"Universal",
    "MCI":"Local"
}

Date_dict = {  
    "JD":["Year","JD"],
    "Int_Date":["Year","Month","Day"],
    "Str_Date":["Date_String"]
}

Function_list = ['Distance', 'Time Calculations', 'Summary']

#Could be a better way to handle the headers and type
d = {'a1': {'b1': 1, 'b2': 2}, 'a2': {'b1': 3, 'b2': 4}}