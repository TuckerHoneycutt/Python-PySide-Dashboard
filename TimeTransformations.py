"""
This script will be used for all Time Conversions as the 
base of the ASCEND tool.
"""

import numpy as np
import pandas as pd
import calendar
from datetime import datetime, timedelta
from operator import attrgetter

time_format = "%H:%M:%S.%f"

def convert_single_epoch2gps(seconds=0, nanoseconds=0): #V&V
    # GPS epoch offset (GPS starts at January 6, 1980)
    gps_date = datetime(1980, 1, 6, 0, 0, 0)
    attrs = ('year', 'month', 'day', 'hour', 'minute', 'second')
    gps_tuple = attrgetter(*attrs)(gps_date)
    
    epoch_seconds = float(seconds) + (int(nanoseconds) / 1e9)
    gps_ns = epoch_seconds - calendar.timegm(gps_tuple)

    # Convert to Unix epoch nanoseconds
    gps_ns = int(gps_ns * 1e9)
    
    return gps_ns

def epoch2gps(seconds=0, nanoseconds=0): #V&V

    # Convert GPS nanoseconds to seconds
    if isinstance(seconds, (list, pd.Series)) and isinstance(nanoseconds, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        epoch = [convert_single_epoch2gps(seconds[i], nanoseconds[i]) for i in range(len(nanoseconds))]   
        return epoch
    elif isinstance(seconds, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        epoch = [convert_single_epoch2gps(seconds=seconds[i]) for i in range(len(seconds))]   
        return epoch
    elif isinstance(nanoseconds, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        epoch = [convert_single_epoch2gps(nanoseconds=nanoseconds[i]) for i in range(len(nanoseconds))]   
        return epoch
    
    else:
        # Otherwise, assume tod is a single time string
        return convert_single_epoch2gps(seconds, nanoseconds)

def epoch2tod(seconds=0, nanoseconds=0): #V&V
    year, jd, ssm = epoch2ssm(seconds=seconds, nanoseconds=nanoseconds)
    tod = ssm2tod(ssm)

    return year, jd, tod

def epoch2ssm(seconds=0, nanoseconds=0): #V&V
    # Convert inputs to numpy arrays for vectorized operations
    seconds_array = np.asarray(seconds)
    nanoseconds_array = np.asarray(nanoseconds)
    
    # Calculate total nanoseconds
    total_nanoseconds = (seconds_array.astype(float) * 1_000_000_000 + nanoseconds_array.astype(int))
    timestamps = pd.to_datetime(total_nanoseconds)

    # Extract year, month, and day from timestamps
    years = timestamps.year
    months = timestamps.month
    days = timestamps.day

    year, jd = intdate2jd(years, months, days)
    
    # Calculate seconds since midnight
    ssm = (timestamps.hour * 3600.0 + timestamps.minute * 60.0 + timestamps.second+(timestamps.microsecond/1000000))

    if type(years)!=int:
        ssm = ssm.tolist()
        
    return year, jd, ssm

def epoch2mci(seconds=0, nanoseconds=0, reftod="hh:mm:ss.s", refmci=0):
    year, jd, tod = epoch2tod(seconds=seconds, nanoseconds=nanoseconds)
    mci = tod2mci(tod, reftod=reftod, refmci=refmci)

    return year, jd, mci
 
def convert_single_gps2epoch(seconds=0, nanoseconds=0): #V&V
    
    gps_date = datetime(1980, 1, 6, 0, 0, 0)
    attrs = ('year', 'month', 'day', 'hour', 'minute', 'second')
    d_tuple = attrgetter(*attrs)(gps_date)
    
    epoch_timestamp = calendar.timegm(d_tuple)
    
    gps_seconds = float(seconds) + (int(nanoseconds) / 1e9)
    epoch_ns = gps_seconds + epoch_timestamp

    # Convert to Unix epoch nanoseconds
    epoch_ns = int(epoch_ns * 1e9)
    
    return epoch_ns

def gps2epoch(seconds=0, nanoseconds=0): #V&V

    # Convert GPS nanoseconds to seconds
    if isinstance(seconds, (list, pd.Series)) and isinstance(nanoseconds, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        epoch = [convert_single_gps2epoch(seconds[i], nanoseconds[i]) for i in range(len(nanoseconds))]   
        return epoch
    elif isinstance(seconds, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        epoch = [convert_single_gps2epoch(seconds=seconds[i]) for i in range(len(seconds))]   
        return epoch
    elif isinstance(nanoseconds, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        epoch = [convert_single_gps2epoch(nanoseconds=nanoseconds[i]) for i in range(len(nanoseconds))]   
        return epoch
    
    else:
        # Otherwise, assume tod is a single time string
        return convert_single_gps2epoch(seconds, nanoseconds)

def gps2tod(seconds=0, nanoseconds=0): #V&V
    nanoseconds=gps2epoch(seconds=seconds, nanoseconds=nanoseconds)
    year, jd, tod = epoch2tod(seconds=0, nanoseconds=nanoseconds)

    return year, jd, tod

def gps2ssm(seconds=0, nanoseconds=0):#V&V
    year, jd, ssm = epoch2ssm(nanoseconds=gps2epoch(seconds, nanoseconds))

    return year, jd, ssm

def gps2mci(seconds=0, nanoseconds=0, reftod="hh:mm:ss.s", refmci=0):
    epoch_ns = gps2epoch(seconds, nanoseconds)
    year, jd, mci = epoch2mci(nanoseconds=epoch_ns, reftod=reftod, refmci=refmci)

    return year, jd, mci
 
def convert_single_tod2epoch(year, jd, tod): #V&V
    """tod is hh:mm:ss.s"""
    year, month, day = jd2intdate(year, jd)
    h, m, s = map(float, tod.split(':'))

    # Create a datetime object for the given date
    date = datetime(year, month, day, int(h), int(m), int(s))
    attrs = ('year', 'month', 'day', 'hour', 'minute', 'second')
    d_tuple = attrgetter(*attrs)(date)
    
    # Convert the datetime object to a timestamp
    epoch_timestamp = calendar.timegm(d_tuple)
    epoch_ns = int(epoch_timestamp * 1e9)+(s*1000000000 -(int(s)*1000000000))

    return epoch_ns

def tod2epoch(year, jd, tod): #V&V
    if isinstance(tod, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        epoch = [convert_single_tod2epoch(year[i], jd[i], tod[i]) for i in range(len(tod))]
        
        return epoch
    else:
        # Otherwise, assume tod is a single time string
        return convert_single_tod2epoch(year, jd, tod)

def tod2gps(year, jd, tod):
    epoch_ns = tod2epoch(year, jd, tod)
    gps_ns = epoch2gps(nanoseconds=epoch_ns)
    
    return gps_ns

def convert_single_tod2ssm(tod):  #V&V Works
    # Split the time string into hours, minutes, and seconds
    h, m, s = map(float, tod.split(':'))
    
    # Convert hours, minutes, and seconds to total seconds
    ssm = h * 3600 + m * 60 + s
    
    return ssm

def tod2ssm(tod): #V&V Works
    """TOD is hh:mm:ss.s"""

    if isinstance(tod, (list, pd.Series)):
        # If tod is a list or pandas Series, apply the conversion to each element
        return [convert_single_tod2ssm(x) for x in tod]
    else:
        # Otherwise, assume tod is a single time string
        return convert_single_tod2ssm(tod)

def tod2mci(tod, reftod, refmci): #V&V
    """Convert time of day to MCI using reference time of day and reference MCI."""
    ssm = tod2ssm(tod)
    return ssm2mci(ssm, reftod, refmci)

def ssm2epoch(year, jd, ssm): #V&V

    tod = ssm2tod(ssm)
    epoch_ns = tod2epoch(year, jd, tod)
    
    return epoch_ns

def ssm2gps(year, jd, ssm):
    gps_ns = epoch2gps(nanoseconds=ssm2epoch(year, jd, ssm))

    return gps_ns

def convert_single_ssm2tod(ssm): #V&V

    # Calculate hours, minutes, and seconds
    hours = int(ssm // 3600)
    minutes = int((ssm % 3600) // 60)
    seconds = ssm % 60

    # Format the time as hh:mm:ss.ss
    return f"{hours:02}:{minutes:02}:{seconds:05.2f}"

def ssm2tod(ssm): #V&V

    if isinstance(ssm, (list, pd.Series)):
        # If ssm is a list or pandas Series, apply the conversion to each element
        return [convert_single_ssm2tod(x) for x in ssm]
    else:
        # Otherwise, assume ssm is a single value
        return convert_single_ssm2tod(float(ssm))

def convert_single_ssm2mci(ssm, reftod, refmci): #V&V
    refssm = tod2ssm(reftod)

    print("Single Input")
    print(ssm)
    print(refssm)
    delta_mci = (float(ssm) - refssm) * 10
    print("delta")
    print(delta_mci)
    
    return float(refmci) + delta_mci

def ssm2mci(ssm, reftod, refmci): #V&V
    
    # Check if inputs are lists or pandas Series
    if isinstance(ssm, (list, pd.Series)):
        print("in ssm2mci list")
        print(ssm)
        # Using list comprehension to process each item
        mci = [convert_single_ssm2mci(ssm[i], reftod, refmci) for i in range(len(ssm))]
        return mci
    else:
        return convert_single_ssm2mci(ssm, reftod, refmci)

def mci2epoch(year, jd, mci, reftod, refmci):
    year, jd, ssm = mci2ssm(year, jd, mci, reftod, refmci)
    epoch_ns = ssm2epoch(year, jd, ssm)
    
    return epoch_ns

def mci2gps(year, jd, mci, reftod, refmci):
    epoch_ns = mci2epoch(year, jd, mci, reftod, refmci)
    gps_ns = epoch2gps(nanoseconds=epoch_ns)  
                   
    return gps_ns

def mci2tod(year, jd, mci, reftod, refmci): #V&V

    year, jd, ssm = mci2ssm(year, jd, mci, reftod, refmci)
    tod = ssm2tod(ssm)

    return year, jd, tod

def mci2ssm(year, jd, mci, reftod, refmci): #V&V
    # Check if inputs are lists or pandas DataFrames
    if isinstance(year, (list, pd.Series)):
        results = [convert_single_mci2ssm(year[i], jd[i], mci[i], reftod, refmci)
            for i in range(len(year))]
        
        # Unzip the results into separate lists
        Year, JD, ssm = zip(*results)
        return list(Year), list(JD), list(ssm)
    
    else:
        return convert_single_mci2ssm(year, jd, mci, reftod, refmci)

def convert_single_mci2ssm(year, jd, mci, reftod, refmci): #V&V
    year, month, day = jd2intdate(int(year), int(jd))
    date_datetime = datetime(year, month, day)
    reftod_datetime = datetime.strptime(reftod, time_format).time()  # Adjust time format if needed

    # Combine into a datetime object
    dt = datetime.combine(date_datetime, reftod_datetime)
    
    seconds_delta = (float(mci) - float(refmci)) / 10

    newdate = dt + timedelta(seconds=seconds_delta)
    
    ssm = (newdate - newdate.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

    return year, jd, ssm

def is_leap_year(year): #V&V
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

def convert_single_jd2intdate(year, jd): #V&V
    """Convert a single year and Julian date to an integer date."""
    Year = int(year)
    jd = int(jd)
    
    if is_leap_year(Year):
        K = 1
    else:
        K = 2
    Month = int((9 * (K + jd)) / 275.0 + 0.98)
    if jd < 32:
        Month = 1
    Day = jd - int((275 * Month) / 9.0) + K * int((Month + 9) / 12.0) + 30
    
    return int(Year), int(Month), int(Day)

def jd2intdate(year, jd): #V&V
    """Convert Julian date to an integer date (year, month, day)."""

    if isinstance(year, (list, pd.Series)) and isinstance(jd, (list, pd.Series)):
        # If both year and jd are lists or pandas Series, apply conversion to each pair
        results = [convert_single_jd2intdate(year[i], jd[i])
            for i in range(len(year))]
        
        # Unzip the results into separate lists
        Year, Month, Day = zip(*results)      
        return list(Year), list(Month), list(Day)
    
    else:
        # Otherwise, assume year and jd are single values
        return convert_single_jd2intdate(year, jd)

def jd2strdate(year, jd): #V&V
    """ will return date as a string 'Month Day, Year' """
        
    Year, Month, Day = jd2intdate(year, jd) 
    
    if isinstance(Month, (list, pd.Series)):
        Date = []
        
        i=0
        while i < len(Month):
            m = calendar.month_name[Month[i]]
            Date.append(str(m)+" " + str(Day[i])+", " + str(Year[i]))
            i = i+1
            
        return Date
    else:
        Month = calendar.month_name[Month]
        
        return str(Month)+" " + str(Day)+", " + str(Year)

def intdate2jd(year, month, day): #V&V
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

def convert_single_strdate2intdate(date): #V&V
    other, Year = date.split(',')
    Month, Day = other.split(' ')
    Month = pd.to_datetime(Month, format='%B').month

    return int(Year), int(Month), int(Day)

def intdate2strdate(year, month, day): #V&V
    """ will return date as a string 'Month Day, Year' """
    
    if isinstance(month, (list, pd.Series)) and isinstance(day, (list, pd.Series)) and isinstance(year, (list, pd.Series)):
        Date = [calendar.month_name[month[i]]+" " + str(day[i])+", " + str(year[i])
            for i in range(len(year))]
        
    elif isinstance(month, (list, pd.Series)) and isinstance(day, (list, pd.Series)):
        Date = [calendar.month_name[month[i]]+" " + str(day[i])+", " + str(year)
            for i in range(len(month))]
        
    elif isinstance(month, (list, pd.Series)):
        Date = [calendar.month_name[month]+" " + str(day[i])+", " + str(year)
            for i in range(len(day))]
    else:
        Date = calendar.month_name[month]+" " + str(day)+", " + str(year)
        
    return Date
    
def strdate2jd(date): #V&V
    """ Input as 'Month day, year' or accept lists/Series of such strings."""
    Year, Month, Day = strdate2intdate(date)
    Year, JD = intdate2jd(Year, Month, Day)
    
    return Year, JD 

def strdate2intdate(date): #V&V
    """ Input as 'Month day, year' or accept lists/Series of such strings."""
    if isinstance(date, (list, pd.Series)):
        Year = []
        Month = []
        Day = []
        
        for d in date:
            y, m, d = convert_single_strdate2intdate(d)
            Year.append(y)
            Month.append(m)
            Day.append(d)
            
        return Year, Month, Day
    else:
        return convert_single_strdate2intdate(date)
     
def MasterTimeConvert(InputUnit, OutputUnit, input1var= np.nan, input2var= np.nan, 
                             input3var= np.nan, input4var= np.nan, indate = 'JD', refput1var= np.nan, 
                             refput2var= np.nan, outdate = 'JD'):

    print(input1var, input2var, input3var, input4var)
    
    if type(input1var) == str:
        if input1var == "":
            input1var = 0
    
        if input2var == "":
            input2var = 0 
    
        if InputUnit == "Date":
            InputUnit = indate
            
        if OutputUnit == "Date":
            OutputUnit = outdate

    if InputUnit != "EPOCH" and InputUnit != "GPS":
        if ((InputUnit != "TOD" and OutputUnit != "SSM") or 
        (InputUnit != "TOD" and OutputUnit != "MCI") or 
        (InputUnit != "SSM" and OutputUnit != "MCI")):
            print("sub")
            if indate != "JD":
                if indate == "Int_Date":
                    input1var, input2var = intdate2jd(int(input1var), int(input2var), 
                                                              int(input3var))
                    input3var = input4var
                    
                elif indate == "Str_Date":
                    input3var = input2var
                    input1var, input2var = strdate2jd(input1var)
                
                InputUnit = "JD"
                indate = "JD"
                
    print("date input")

    if InputUnit == "EPOCH": 
        if OutputUnit == "GPS":
            res1 = epoch2gps(input1var, input2var)
            
        elif OutputUnit == "TOD":
            res1, res2, res3 = epoch2tod(input1var, input2var) 
            
        elif OutputUnit == "SSM":

            res1, res2, res3 = epoch2ssm(input1var, input2var)  

        elif OutputUnit == "MCI":
            res1, res2, res3 = epoch2mci(input1var, input2var, refput1var, refput2var)  
            
        elif OutputUnit == "EPOCH":
            res1 = (float(input1var)*1e9) + (int(input2var))

    elif InputUnit == "GPS":
        if OutputUnit == "EPOCH":
            res1 = gps2epoch(input1var, input2var)
            
        elif OutputUnit == "TOD":
            res1, res2, res3 = gps2tod(input1var, input2var) 
            
        elif OutputUnit == "SSM":
            res1, res2, res3 = gps2ssm(input1var, input2var)  
            
        elif OutputUnit == "MCI":
            res1, res2, res3 = gps2mci(input1var, input2var, refput1var, refput2var)
        
        elif OutputUnit == "GPS":
            res1 = (float(input1var)*1e9) + (int(input2var))
            
    elif InputUnit == "TOD":
        if OutputUnit == "EPOCH":
            res1 = tod2epoch(input1var, input2var, input3var)
            
        elif OutputUnit == "GPS":
            res1 = tod2gps(input1var, input2var, input3var) 
            
        elif OutputUnit == "SSM":
            
            if pd.isna(input3var):
                res1 = tod2ssm(input1var)
                return res1
            
            else:
                print(input1var, input2var)
                res1 = input1var
                res2 = input2var
                res3 = tod2ssm(input3var)  
            
        elif OutputUnit == "MCI":
            if type(input3var) != list: 
                if pd.isna(input3var):
                    res1 = tod2mci(input1var, refput1var, refput2var)
                    return res1
            
            else:
                res1 = input1var
                res2 = input2var
                res3 = tod2mci(input3var, refput1var, refput2var)

        elif OutputUnit == "TOD":
            res1 = input1var
            res2 = input2var
            res3 = input3var
            
    elif InputUnit == "SSM":
        if OutputUnit == "EPOCH":
            res1 = ssm2epoch(input1var, input2var, input3var)
            
        elif OutputUnit == "GPS":
            res1 = ssm2gps(input1var, input2var, input3var) 
            
        elif OutputUnit == "TOD":
            print('Converting to SSM')
            print(input3var)
            print(type(input3var))

            res1 = input1var
            res2 = input2var
            res3 = ssm2tod(input3var)  
            
        elif OutputUnit == "MCI":
            if type(input3var) != list: 
                if pd.isna(input3var):
                    res1 = ssm2mci(input1var, refput1var, refput2var)
                    return res1
            
            else:
                res1 = input1var
                res2 = input2var
                res3 = ssm2mci(input3var, refput1var, refput2var)
        
        elif OutputUnit == "SSM":
            res1 = input1var
            res2 = input2var
            res3 = input3var
                
    elif InputUnit == "MCI":
        print("in MCI")
        if OutputUnit == "EPOCH":
            res1 = mci2epoch(input1var, input2var, input3var, refput1var, refput2var)
            
        elif OutputUnit == "GPS":
            res1 = mci2gps(input1var, input2var, input3var, refput1var, refput2var) 
            
        elif OutputUnit == "TOD":
            res1, res2, res3 = mci2tod(input1var, input2var, input3var, refput1var, refput2var)  
            
        elif OutputUnit == "SSM":
            res1, res2, res3 = mci2ssm(input1var, input2var, input3var, refput1var, refput2var)
        
        elif OutputUnit == "MCI":
            res1, res2, res3 = input1var, input2var, input3var

    if OutputUnit == "Int_Date":
        res1, res2, res3 = jd2intdate(input1var, input2var)
        
        return res1, res2, res3
    
    elif OutputUnit == "Str_Date":
        res1 = jd2strdate(input1var, input2var) 
        
        return res1
    
    elif OutputUnit == "JD":
        res1, res2 = input1var, input2var
        
        return res1, res2
        
    if OutputUnit != "EPOCH" and OutputUnit != "GPS":
        #if indate == "JD":
        if outdate == "Int_Date":
            res1date, res2date, res3date = jd2intdate(res1, res2)
            
            return res1date, res2date, res3date, res3
        
        elif outdate == "Str_Date":
            res1date = jd2strdate(res1, res2)

            return res1date, res3
        else:    
            return res1, res2, res3
    
    else:
        return res1