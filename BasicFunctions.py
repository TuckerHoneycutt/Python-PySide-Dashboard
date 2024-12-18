# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 08:57:06 2024

@author: kayla.green
"""
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import TimeTransformations as TT
import WindowConfigFile as wc
import HeaderDictionary as head
from tkinter import filedialog
import pandas as pd
import os
from tkinter import messagebox
import CoordinateTransformations as CC
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

def handle_file_conversion():
    """Handle file selection and update filenames and columns."""
    FileName = filedialog.askopenfilename()
    current_directory = filedialog.askdirectory()

    file_name = os.path.splitext(os.path.basename(FileName))[0]
    NewFileName = os.path.join(current_directory, file_name + "_Imported")

    if ".xlsx" in FileName:
        df = pd.read_excel(FileName)
    elif ".csv" in FileName:
        df = pd.read_csv(FileName).convert_dtypes()
    
    return FileName, NewFileName, df

def DistanceBetweenPositions(Point1_x, Point1_y, Point2_x, Point2_y, Point1_z=0, Point2_z=0, referenceFrame = ""):
    #Returns Distance in meters for UTM, LLA, REA, and RUV.
    #All other returns are in the unit given
    
    if referenceFrame == "UTM":
        #convert to ECEF
        Point1_x, Point1_y, Point1_z = CC.utm2ecef(Point1_x, Point1_y, Point1_z)
        Point2_x, Point2_y, Point2_z = CC.utm2ecef(Point2_x, Point2_y, Point2_z)
        
    elif referenceFrame == "LLA":
        #Convert to ECEF
        Point1_x, Point1_y, Point1_z = CC.lla2ecef(Point1_x, Point1_y, Point1_z)
        Point2_x, Point2_y, Point2_z = CC.lla2ecef(Point2_x, Point2_y, Point2_z)
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [Point1_x, Point1_y, Point2_x, Point2_y])
        
        #Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of Earth in kilometers (change to 3956 for miles)
        r = 6371.0  #Km
        horizontal_distance = r * c
        horizontal_distance = horizontal_distance * 1000  #meteres
        
        # Calculate the vertical distance
        vertical_distance = Point1_z - Point2_z
        
        # Use Pythagorean theorem to calculate the total distance
        DistanceCalculated = math.sqrt(horizontal_distance**2 + vertical_distance**2)
        
        return DistanceCalculated #meters
        
    elif referenceFrame == "REA":
        Point1_x, Point1_y, Point1_z = CC.rea2enu(Point1_x, Point1_y, Point1_z)
        Point2_x, Point2_y, Point2_z = CC.rea2enu(Point2_x, Point2_y, Point2_z)
        
    elif referenceFrame == "RUV":
        Point1_x, Point1_y, Point1_z = CC.ruv2enu(Point1_x, Point1_y, Point1_z)
        Point2_x, Point2_y, Point2_z = CC.ruv2enu(Point2_x, Point2_y, Point2_z)   

    #regular distance formula
    DistanceCalculated = math.dist([Point1_x, Point1_y, Point1_z], [Point2_x, Point2_y, Point2_z])
        
    return DistanceCalculated

def TimeCalculations(TimeCol, df, Type="UpdateRate", TimeCol2="", newcolName="", groupCol=""):
    """
    Function to perform time-based calculations (UpdateRate, Delta) on a DataFrame.

    Args:
    - TimeCol (str): The name of the column on which calculations will be performed.
    - df (pd.DataFrame): The DataFrame to perform calculations on.
    - Type (str): The type of calculation. Can be "UpdateRate" or "Delta".
    - TimeCol2 (str): A second time column used for "Delta" type calculations.
    - newcolName (str): Name of the new column for the result (optional).
    - groupCol (str): Column for grouping the DataFrame before applying the calculations (optional).
    
    Returns:
    - pd.DataFrame: DataFrame with the new calculated column(s).
    """
    if groupCol == "":
        # If no grouping column is provided, apply calculations directly to the entire DataFrame
        df = TimeCalculations_math(TimeCol, df, Type=Type, TimeCol2=TimeCol2, newcolName=newcolName)
    else:
        # If a grouping column is provided, apply the calculations for each group
        groupdf = df.groupby(groupCol)
        # Apply the function for each group
        df = groupdf.apply(lambda group: TimeCalculations_math(TimeCol, group, Type=Type, 
                                                                TimeCol2=TimeCol2, newcolName=newcolName))

    return df

def TimeCalculations_math(TimeCol, df, Type="UpdateRate", TimeCol2="", newcolName=""):
    """
    Performs the actual calculation (either UpdateRate or Delta) on the DataFrame.

    Args:
    - TimeCol (str): The name of the column for which the calculation is performed.
    - df (pd.DataFrame): The DataFrame to perform the calculation on.
    - Type (str): The type of calculation. Can be "UpdateRate" or "Delta".
    - TimeCol2 (str): A second time column used for "Delta" type calculations.
    - newcolName (str): The name of the new column for the result (optional).
    
    Returns:
    - pd.DataFrame: DataFrame with the new calculated column(s).
    """
    if Type == "UpdateRate":
        # If we have a new column name, use it, otherwise create a default one
        if newcolName != "":
            df[newcolName] = df[TimeCol].diff()
        else:
            df[TimeCol + " update rate"] = df[TimeCol].diff()
                
    elif Type == "Delta":
        # If we have a second column for delta calculations, subtract the values in TimeCol2
        if newcolName != "":
            df[newcolName] = df[TimeCol] - df[TimeCol2]
        else:
            df[TimeCol + " Delta"] = df[TimeCol] - df[TimeCol2]
    
    elif Type == "Stats":
        describe_A = df[TimeCol].describe()
        print(describe_A)
        
    return df

# Haversine function to calculate the great-circle distance
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Distance in kilometers
    return R * c