# -*- coding: utf-8 -*-
"""
Spyder Editor

This script will be used for all Coordanate Conversion as the 
base of the ASCEND tool.
"""
#epoch
#gps
#TOD
#SSM
#JD
#Date
#string_date
#MIC

import numpy as np
import pandas as pd
import math
import calendar
import time
import datetime
from datetime import datetime, timedelta

time_format = "%H:%M:%S.%f"

def epoch2gps(seconds=0, nanoseconds=0):
    # GPS epoch offset (GPS starts at January 6, 1980)
    
    # Convert inputs to numpy arrays for vectorized operations
    seconds_array = np.asarray(seconds)
    nanoseconds_array = np.asarray(nanoseconds)
    
    # Ensure nanoseconds is treated as an array
    nanoseconds_array = np.where(nanoseconds_array is None, 0, nanoseconds_array)

    # Calculate total nanoseconds
    total_nanoseconds = (seconds_array.astype(float) * 1_000_000_000 + nanoseconds_array.astype(int))
    gps_epoch_offset = 10_368_000_000 * 1_000_000_000  # 10^9 seconds in nanoseconds
    gps_ns = total_nanoseconds + gps_epoch_offset
    
    gps_ns = gps_ns.tolist()
    
    return gps_ns

def epoch2tod(seconds=0, nanoseconds=0):
    year, jd, ssm = epoch2ssm(seconds=seconds, nanoseconds=nanoseconds)
    tod = ssm2tod(ssm)

    return year, jd, tod

def epoch2ssm(seconds=0, nanoseconds=0):
    
    # Convert inputs to numpy arrays for vectorized operations
    seconds_array = np.asarray(seconds)
    nanoseconds_array = np.asarray(nanoseconds)
    
    # Calculate total nanoseconds
    total_nanoseconds = (seconds_array.astype(float) * 1_000_000_000 + nanoseconds_array.astype(int))
    print(total_nanoseconds)
    timestamps = pd.to_datetime(total_nanoseconds)

    # Extract year, month, and day from timestamps
    years = timestamps.year
    months = timestamps.month
    days = timestamps.day

    year, jd = intdate2jd(years, months, days)

    if type(years)==int:
        ssm = (timestamps.hour * 3600.0 + timestamps.minute * 60.0 + timestamps.second+(timestamps.microsecond/1000000))
    else:
        # Calculate seconds since midnight
        ssm = [(ts.hour * 3600 + ts.minute * 60 + ts.second+(timestamps.microsecond/1000000)) for ts in timestamps]

    return year, jd, ssm

def epoch2mci(seconds=0, nanoseconds=0, reftod="hh:mm:ss.s", refmci=0):
    year, jd, tod = epoch2tod(seconds=seconds, nanoseconds=nanoseconds)
    mci = tod2mci(tod, reftod=reftod, refmci=refmci)

    return year, jd, mci
 
def convert_single_gps2epoch(seconds=0):
    gps_epoch = datetime(1980, 1, 6)
    
    # Calculate the corresponding Unix epoch time
    epoch_time = gps_epoch + timedelta(seconds=seconds)
    
    # Convert to Unix epoch nanoseconds
    epoch_ns = int(epoch_time.timestamp() * 1e9)

def gps2epoch(seconds=0, nanoseconds=0):
    # Convert GPS nanoseconds to seconds
    gps_seconds = float(seconds) + (int(nanoseconds) / 1e9)
    
    if isinstance(gps_seconds, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        return [convert_single_gps2epoch(x) for x in gps_seconds]
    else:
        # Otherwise, assume tod is a single time string
        return convert_single_gps2epoch(gps_seconds)


def gps2tod(seconds=0, nanoseconds=0):
    nanoseconds=gps2epoch(seconds=seconds, nanoseconds=nanoseconds)
    print(nanoseconds)
    year, jd, tod = epoch2tod(seconds=0, nanoseconds=nanoseconds)

    return year, jd, tod

def gps2ssm(seconds=0, nanoseconds=0):
    year, jd, ssm = epoch2ssm(nanoseconds=gps2epoch(seconds, nanoseconds))

    return year, jd, ssm

def gps2mci(seconds=0, nanoseconds=0, reftod="hh:mm:ss.s", refmci=0):
    year, jd, mci = epoch2mci(nanoseconds=gps2epoch(seconds, nanoseconds))

    return year, jd, mci
 
def tod2epoch(year, jd, tod):
    """tod is hh:mm:ss.s"""
    ssm = tod2ssm(tod)
    epoch_ns = ssm2epoch(year, jd, ssm)
    
    return epoch_ns

def tod2gps(year, jd, tod):
    print("working")
    epoch_ns = tod2epoch(year, jd, tod)
    gps_ns = epoch2gps(nanoseconds=epoch_ns)
    
    return gps_ns

def convert_single_tod2ssm(tod):
    print(tod)
    # Split the time string into hours, minutes, and seconds
    h, m, s = map(float, tod.split(':'))
    
    # Convert hours, minutes, and seconds to total seconds
    ssm = h * 3600 + m * 60 + s
    
    return ssm

def tod2ssm(tod):
    """TOD is hh:mm:ss.s"""

    if isinstance(tod, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        return [convert_single_tod2ssm(x) for x in tod]
    else:
        # Otherwise, assume tod is a single time string
        return convert_single_tod2ssm(tod)


def convert_single_tod2mci(tod, reftod_datetime, refmci):
    # Convert the string timestamp to a datetime object
    tod_datetime = datetime.strptime(tod, time_format)
    
    # Calculate the difference between the two timestamps
    delta = reftod_datetime - tod_datetime
    
    # Convert delta to seconds and calculate MCI
    mci = tod2ssm(str(delta)) * 10
    
    return mci + refmci
    
def tod2mci(tod, reftod, refmci):
    """Convert time of day to MCI using reference time of day and reference MCI."""

    # Convert reference time of day to datetime object
    reftod_datetime = datetime.strptime(reftod, time_format)

    if isinstance(tod, (list, pd.Series)):
        print("is list")
        # If tod is a list or pandas Series, apply the conversion to each element
        return [convert_single_tod2mci(x, reftod_datetime, refmci) for x in tod]
    else:
        print("not list")
        # Otherwise, assume tod is a single time string
        return convert_single_tod2mci(tod, reftod_datetime, refmci)

def ssm2epoch(year, jd, ssm):
    year, month, day = jd2intdate(year, jd)
    
    # Create a datetime object for the given date
    date = datetime(year, month, day)
    
    # Add the seconds since midnight to the datetime object
    date_with_seconds = date + timedelta(seconds=float(ssm))
    
    # Convert the datetime object to a timestamp
    epoch_timestamp = int(time.mktime(date_with_seconds.timetuple()))
    epoch_ns = int(epoch_timestamp * 1e9)
    
    return epoch_ns

def ssm2gps(year, jd, ssm):
    gps_ns = epoch2gps(nanoseconds=ssm2epoch(year, jd, ssm))

    return gps_ns

def convert_single_ssm2tod(ssm):

    # Calculate hours, minutes, and seconds
    hours = int(ssm // 3600)
    minutes = int((ssm % 3600) // 60)
    seconds = ssm % 60

    # Format the time as hh:mm:ss.ss
    return f"{hours:02}:{minutes:02}:{seconds:05.2f}"

def ssm2tod(ssm):
    print(ssm)
    if isinstance(ssm, (list, pd.Series)):
        # If ssm is a list or pandas Series, apply the conversion to each element
        return [convert_single_ssm2tod(x) for x in ssm]
    else:
        # Otherwise, assume ssm is a single value
        return convert_single_ssm2tod(ssm)

def ssm2mci(ssm, reftod, refmci):

    tod = ssm2tod(ssm)
    mci = tod2mci(tod, reftod, refmci)
    
    return mci

def mci2epoch(year, jd, mci, reftod, refmci):
    year, jd, ssm = mci2ssm(year, jd, mci, reftod, refmci)
    epoch_ns = ssm2epoch(year, jd, ssm)
    
    return epoch_ns

def mci2gps(year, jd, mci, reftod, refmci):
    print("working")
    epoch_ns = mci2epoch(year, jd, mci, reftod, refmci)
    gps_ns = epoch2gps(nanoseconds=epoch_ns)  
                   
    return gps_ns

def mci2tod(year, jd, mci, reftod, refmci):

    year, month, day = jd2intdate(year, jd)
    date_datetime = datetime(year, month, day)
    reftod_datetime = datetime.strptime(reftod, time_format).time()

    # Combine into a datetime object
    #dt = datetime.combine(date_datetime, reftod_datetime)
    
    # Get the timestamp
    #timestamp = dt.timestamp()
    
    newdate = reftod_datetime + timedelta(seconds=mci*10)

    print(newdate)
    
    return newdate

def is_leap_year(year):
    """ if year is a leap year return True
        else return False """
        
    # Convert input to a NumPy array for easy handling of lists and Series
    years_array = np.asarray(year)
    
    # Function to check leap year for a single year
    def check_leap(y):
        if int(y) % 100 == 0:
            return int(y) % 400 == 0
        return int(y) % 4 == 0

    # Apply the leap year check to each year in the array
    leap_years = np.vectorize(check_leap)(years_array)

    # Return results as a list or single boolean
    if leap_years.size == 1:
        return leap_years.item()  # Return single boolean
    return leap_years.tolist()  # Return list of booleans

def mci2ssm(year, jd, mci, reftod, refmci):
    print("working")
    Year = 0
    JD = 0
    mci = 0
    return Year, JD, mci

def convert_single_jd2intdate(year, jd):
    """Convert a single year and Julian date to an integer date."""
    year = int(year)
    jd = int(jd)
    
    if is_leap_year(year):
        K = 1
    else:
        K = 2
    Month = int((9 * (K + jd)) / 275.0 + 0.98)
    if jd < 32:
        Month = 1
    Day = jd - int((275 * Month) / 9.0) + K * int((Month + 9) / 12.0) + 30
    
    return year, Month, Day

def jd2intdate(year, jd):
    """Convert Julian date to an integer date (year, month, day)."""

    if isinstance(year, (list, pd.Series)) and isinstance(jd, (list, pd.Series)):
        # If both year and jd are lists or pandas Series, apply conversion to each pair
        return [convert_single_jd2intdate(y, j) for y, j in zip(year, jd)]
    else:
        # Otherwise, assume year and jd are single values
        return convert_single_jd2intdate(year, jd)

def jd2strdate(year, jd):
    """ will return date as a string 'Month Day, Year' """
        
    Year, Month, Day = jd2intdate(year, jd) 
    Month = calendar.month_name[Month]


    return str(Month)+" " + str(Day)+", " + str(Year)

def intdate2jd(year, month, day):
    """Return year and Julian date."""
    year = np.asarray(year)
    month = np.asarray(month)
    day = np.asarray(day)

    # Initialize the K array
    K = np.where(is_leap_year(year), 1, 2)
    
    # Calculate Julian date
    jd = (275 * month) // 9 - K * ((month + 9) // 12) + day - 30

    # Return results as lists or single values
    if year.size == 1:
        return year.item(), jd.item()  # Return single year and Julian date
    return year.tolist(), jd.tolist()  # Return lists for multiple values

def intdate2strdate(month, day, year):
    """ will return date as a string 'Month Day, Year' """
    
    month = calendar.month_name[month]

    return str(month)+" " + str(day)+", " + str(year)

def strdate2jd():
    Year = 0
    Month = 0
    JD = 0
    return Year, Month, JD

def strdate2intdate():
    Year = 0
    Month = 0
    Day = 0

    return Year, Month, Day
    
def MasterTimeConvert(InputUnit, OutputUnit, input1var= np.nan, input2var= np.nan, 
                             input3var= np.nan, input4var= np.nan, indate = 'JD', refput1var= np.nan, 
                             refput2var= np.nan, outdate = 'JD'):
    
    if input1var == "":
        input1var = 0

    if input2var == "":
        input2var = 0 

    if InputUnit == "EPOCH": 
        if OutputUnit == "GPS":
            res1 = epoch2gps(input1var, input2var)
            
        elif OutputUnit == "TOD":

            res1, res2, res3 = epoch2tod(input1var, input2var) 
            
        elif OutputUnit == "SSM":

            res1, res2, res3 = epoch2ssm(input1var, input2var)  

        elif OutputUnit == "MCI":
            res1, res2, res3 = epoch2mci(input1var, input2var, refput1var, refput2var)  
        
    elif InputUnit == "GPS":
        if OutputUnit == "EPOCH":
            res1 = gps2epoch(input1var, input2var)
            
        elif OutputUnit == "TOD":
            res1, res2, res3 = gps2tod(input1var, input2var) 
            
        elif OutputUnit == "SSM":
            res1, res2, res3 = gps2ssm(input1var, input2var)  
            
        elif OutputUnit == "MCI":
            res1, res2, res3 = gps2mci(input1var, input2var, refput1var, refput2var)
            
    elif InputUnit == "TOD":
        if OutputUnit == "EPOCH":
            res1 = tod2epoch(input1var, input2var, input3var)
            
        elif OutputUnit == "GPS":
            res1 = tod2gps(input1var, input2var, input3var) 
            
        elif OutputUnit == "SSM":
            res1 = input1var
            res2 = input2var
            res3 = tod2ssm(input3var)  
            
        elif OutputUnit == "MCI":
            res1, res2, res3 = tod2mci()
            
    elif InputUnit == "SSM":
        if OutputUnit == "EPOCH":
            res1 = ssm2epoch(input1var, input2var, input3var)
            
        elif OutputUnit == "GPS":
            res1 = ssm2gps(input1var, input2var, input3var) 
            
        elif OutputUnit == "TOD":
            res1 = input1var
            res2 = input2var
            res3 = ssm2tod(input3var)  
            
        elif OutputUnit == "MCI":
            res1, res2, res3 = ssm2mci()
    
    elif InputUnit == "MCI":
        if OutputUnit == "EPOCH":
            res1 = mci2epoch()
            
        elif OutputUnit == "GPS":
            res1 = mci2gps() 
            
        elif OutputUnit == "TOD":
            res1, res2, res3 = mci2tod()  
            
        elif OutputUnit == "SSM":
            res1, res2, res3 = mci2ssm()
    
    elif InputUnit == "JD":
        if OutputUnit == "Int_Date":
            res1, res2, res3 = jd2intdate()
            
        elif OutputUnit == "Str_Date":
            res1 = jd2intdate() 
            
    elif InputUnit == "Int_Date":
        if OutputUnit == "JD":
            res1, res2, res3 = intdate2jd()
            
        elif OutputUnit == "Str_Date":
            res1 = intdate2strdate()       
    
    elif InputUnit == "Str_Date":
        if OutputUnit == "JD":
            res1, res2 = strdate2jd()
            
        elif OutputUnit == "Int_Date":
            res1, res2, res3 = strdate2intdate() 
                    
    if OutputUnit != "EPOCH" and OutputUnit != "GPS":
        print("not EPOCH or GPS")
        print(InputUnit)
        if InputUnit != "JD" and InputUnit != "Int_Date" and InputUnit != "Str_Date":
            if outdate == "Int_Date":
                res1date, res2date, res3date = jd2intdate()
                
            elif outdate == "Str_Date":
                res1date = jd2strdate()
                
        return res1, res2, res3
    
    else:
        print("only one results")
        return res1