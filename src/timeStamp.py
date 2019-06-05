# Automatic scheduler for CMU PreCollege Program

import sys
import math

# Class to handle times.
class TimeStamp:

    # Reference day in order to keep track of which day each TimeStamp is
    # The first day of the year 2000 was a Saturday (6 = Saturday)
    referenceYear = 2000
    referenceDay = 6

    # Dictionary of day names to their ints
    dayNameToInt = {
        "Sunday"   : 0,
        "Monday"   : 1,
        "Tuesday"  : 2,
        "Wednesday": 3,
        "Thursday" : 4,
        "Friday"   : 5,
        "Saturday" : 6
    }

    # Dictionay of day ints to their names
    dayIntToName = {
        0 : "Sunday",
        1 : "Monday",
        2 : "Tuesday",
        3 : "Wednesday",
        4 : "Thursday",
        5 : "Friday",
        6 : "Saturday"
    }

    # Time Constructor
    def __init__(self, year = 2018, month = 1, day = 1, hour = 0, minute = 0):

        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
    
    # Convert time to string
    def __repr__(self):

        # Construct the strings for each part of the time
        monthString = str(self.month)
        if len(monthString) == 1:
            monthString = "0" + monthString

        dayString = str(self.day)
        if len(dayString) == 1:
            dayString = "0" + dayString
        
        yearString = str(self.year)
        
        hourString = str(self.hour)
        if len(hourString) == 1:
            hourString = "0" + hourString

        minuteString = str(self.minute)
        if len(minuteString) == 1:
            minuteString = "0" + minuteString
        
        # Construct the date and time part
        date = monthString + "/" + dayString + "/" + yearString
        time = hourString + ":" + minuteString

        # Combine the two strings as the output
        return date + " " + time
    
    # Determine what day of the week the timeStamp is
    def determineDayOfWeek(self):

        # How many days are between the reference date and the current date
        totalDays = 0

        # Counter for the current year we are analyzing
        currentYear = TimeStamp.referenceYear

        # Counter for the current month we are analyzing
        currentMonth = 1

        # Determine how many days we are passed the reference day
        # Start by lining up the currentYear to the TimeStamp year
        while currentYear != self.year:
            totalDays += TimeStamp.determineDaysInYear(currentYear)
            currentYear += 1
        
        # Then line up the months
        while currentMonth != self.month:
            totalDays += TimeStamp.determineDaysInMonth(currentYear, currentMonth)
            currentMonth += 1
        
        # Then add the extra days
        totalDays += (self.day - 1)

        # Now determine what day of the week it is
        dayOfTheWeek = (totalDays + TimeStamp.referenceDay) % 7
        return dayOfTheWeek

    # In order to input a time, it must be in this format: MM/DD/YYYY HH:mm (Where MM, DD, HH, and mm are all two digit numbers)
    @staticmethod
    def createTimeFromString(string):
        
        # Try creating the time
        try:
            month  = int(string[0 : 2])
            day    = int(string[3 : 5])
            year   = int(string[6 : 10])
            hour   = int(string[11 : 13])
            minute = int(string[14 : 16])
            return TimeStamp(year, month, day, hour, minute)
        except:
            print("ERROR: Unable to parse " + string + " as a time")
            sys.exit()

    # Determine how many days are in this month
    @staticmethod
    def determineDaysInMonth(year, month):

        # January
        if month == 1: return 31
        
        # February
        if month == 2:
            if (year % 4) == 0 and ((year % 100) != 0 or (year % 400) == 0):
                return 29
            return 28
        
        # March
        if month == 3: return 31
        
        # April
        if month == 4: return 30
        
        # May
        if month == 5: return 31
        
        # June
        if month == 6: return 30

        # July
        if month == 7: return 31

        # August
        if month == 8: return 31

        # September
        if month == 9: return 30

        # October
        if month == 10: return 31

        # November
        if month == 11: return 30

        # December
        if month == 12: return 31
    
    # Determine how many days are in a certain year
    @staticmethod
    def determineDaysInYear(year):

        # Account for leap years.
        if (year % 4) == 0 and ((year % 100) != 0 or (year % 400) == 0):
            return 366
        return 365
