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
    def __init__(self, text):

        # The text used to construct this conflict
        self.text = text

        # Split the text into the start and end times
        splitText = self.text.split(" - ")

        # Return an error if the conflict doesn't have a start and end time
        if len(splitText) != 2:
            print("ERROR: Unable to parse " + self.text + " as conflict")
            sys.exit()

        # Extract the start time of the conflict
        self.startTime = TimeStamp.createTimeFromString(splitText[0])
        self.endTime = TimeStamp.createTimeFromString(splitText[1])
    
    # Convert the Conflict to a string
    def __repr__(self):

        return str(self.startTime) + " - " + str(self.endTime)
    
    # Determine if 2 conflicts overlap
    @staticmethod
    def doConflictsOverlap(conflict1, conflict2):

        # If either the start time or end time of conflict1 is inside conflict 2, the conflicts overlap.
        if conflict1.startTime > conflict2.startTime and conflict1.startTime < conflict2.endTime: return True
        if conflict1.endTime > conflict2.startTime and conflict1.endTime < conflict2.endTime: return True

        # If the start time is before conflict2 start and after conflict2 end time, the conflicts overlap
        if conflict1.startTime < conflict2.startTime and conflict1.endTime > conflict2.endTime: return True
        
        # If none of the above statements are true, return false
        return False


# Class to handle events which occur continuously
class RecurringConflict:

    # Constructor Text is in format "Day - HH:mm - HH:mm" where Day is the day of the week spelled out and capitalized and
    #   HH:mm - HH:mm describes the start and end time for the conflict
    def __init__(self, text):
        
        # The text the RecurringConflict is based on
        self.text = text

        # Split the text into its components
        splitText = text.split(" - ")

        # return an error if all the required parts of the conflict weren't found
        if len(splitText) != 3:
            print("ERROR: Unable to parse "  + self.text + " as a recurring conflict")
            sys.exit()

        # Get the day of the week for this conflict
        try:
            self.day = TimeStamp.dayNameToInt[splitText[0]]
        except:
            print("ERROR: \"" + splitText[0] + "\" from recurring conflict input \"" + self.text + "\" unable to be parsed as a day. Check capitalization and spelling.")
            sys.exit()
        
        # Get the start time for this conflict
        try:
            self.startHour   = int(splitText[1][0:2])
            self.startMinute = int(splitText[1][3:5])
            self.endHour     = int(splitText[2][0:2])
            self.endMinute   = int(splitText[2][3:5])
        except:
            print("ERROR: Unable to parse the times for " + self.text + ". Check formatting again")
    
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

