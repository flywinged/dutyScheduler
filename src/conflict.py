# Automatic scheduler for CMU PreCollege Program

import sys
from timeStamp import TimeStamp

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


# Class to handle events which occur continuously
class RecurringConflict(Conflict):

    # Constructor
    def __init__(self, text):
        Conflict.__init__(self, text)


# Class to handle single events
class SingleConflict(Conflict):

    # Constructor
    def __init__(self, text):
        Conflict.__init__(self, text)

    # Determine the day of the week
    def determineDayOfWeek(self, text):
        pass

# conflictOne = RecurringConflict("Monday(03:00-21:54)")
conflictTwo = SingleConflict("04/14/2019 08:30 - 04/14/2019 11:00")
