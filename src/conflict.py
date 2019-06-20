# Automatic scheduler for CMU PreCollege Program

import sys
from src.timeStamp import TimeStamp

# Determine if a string represents and integer
def representsInt(string):
    try: 
        int(string)
        return True
    except ValueError:
        return False

# Class to handle scheduling conflicts
class Conflict:

    # Constructor. Text format is: "startTime - endTime" (start and endTime are in the same format as a timestamp)
    def __init__(self, startTimeStampText, endTimeStampText, conflictName = "No Name"):

        # Extract the start time of the conflict
        self.startTime = TimeStamp.createTimeFromString(startTimeStampText)
        self.endTime = TimeStamp.createTimeFromString(endTimeStampText)
        self.conflictName = conflictName
    
    # Convert the Conflict to a string
    def __repr__(self):

        return str(self.startTime) + " - " + str(self.endTime)
    
    # Determine if 2 conflicts overlap
    @staticmethod
    def doConflictsOverlap(conflict1, conflict2):

        # If either the start time or end time of conflict1 is inside conflict 2, the conflicts overlap.
        if conflict1.startTime >= conflict2.startTime and conflict1.startTime <= conflict2.endTime: return True
        if conflict1.endTime >= conflict2.startTime and conflict1.endTime <= conflict2.endTime: return True

        # If the start time is before conflict2 start and after conflict2 end time, the conflicts overlap
        if conflict1.startTime <= conflict2.startTime and conflict1.endTime >= conflict2.endTime: return True
        
        # If none of the above statements are true, return false
        return False


# Class to handle events which occur continuously
class RecurringConflict:

    # Constructor Text is in format "Day - HH:mm - HH:mm" where Day is the day of the week spelled out and capitalized and
    #   HH:mm - HH:mm describes the start and end time for the conflict
    def __init__(self, dayText, startTimeText, endTimeText, conflictName = "No Name"):

        self.conflictName = conflictName

        # Get the day of the week for this conflict
        try:
            self.day = TimeStamp.dayNameToInt[dayText]
        except:
            print("ERROR: \"" + dayText + "\" from recurring conflict input unable to be parsed as a day. Check capitalization and spelling.")
            sys.exit()
        
        # Get the start time for this conflict
        try:
            self.startHour   = int(startTimeText[0:2])
            self.startMinute = int(startTimeText[3:5])
            self.endHour     = int(endTimeText[0:2])
            self.endMinute   = int(endTimeText[3:5])
        except:
            print("ERROR: Unable to parse the times for " + dayText + "," + startTimeText + "," + endTimeText + ". Check formatting again")
            sys.exit()

    # Convert the weeklyConflict to a string
    def __repr__(self):

        # Construct the start time string
        startHourString = str(self.startHour)
        if len(startHourString) == 1:
            startHourString = "0" + startHourString

        startMinuteString = str(self.startMinute)
        if len(startMinuteString) == 1:
            startMinuteString = "0" + startMinuteString
        
        startTimeString = startHourString + ":" + startMinuteString

        # Construct the end time string
        endHourString = str(self.endHour)
        if len(endHourString) == 1:
            endHourString = "0" + endHourString

        endMinuteString = str(self.endMinute)
        if len(endMinuteString) == 1:
            endMinuteString = "0" + endMinuteString
        
        endTimeString = endHourString + ":" + endMinuteString

        return TimeStamp.dayIntToName[self.day] + ": " + startTimeString + " - " + endTimeString

