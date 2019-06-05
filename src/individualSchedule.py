# Automatic scheduler for CMU PreCollege Program

from src.timeStamp import TimeStamp
from src.conflict import Conflict

# Class for handling a schedule for an individual
class IndividualSchedule:

    # Constructor
    def __init__(self, name):
        
        # Define who the schedule is for
        self.name = name

        # Attributes for the individual schedule
        self.floor = None
        self.building = None
        self.weeklyConflicts = None
        self.singleConflicts = None
    
    # Print function
    def __repr__(self):

        # Set the output
        printString = ""

        # Header
        printString += "Schedule for: {0}\n".format(self.name)

        # Add the Building and Floor components
        printString += "Building: {0}\n".format(self.building)
        printString += "Floor: {0}\n".format(self.floor)
        printString += "Weekly Conflicts: " + str(self.weeklyConflicts) + "\n"
        printString += "Single Conflicts: " + str(self.singleConflicts) + "\n"

        return printString
    
    # Set the individual's floor
    def setFloor(self, floor):
        self.floor = floor
    
    # Set the individual's building
    def setBuilding(self, building):
        self.building = building
    
    # Set the individual's weekly conflicts
    def setWeeklyConflicts(self, weeklyConflicts):
        self.weeklyConflicts = weeklyConflicts

    # Set the individual's single conflicts
    def setSingleConflicts(self, singleConflicts):
        self.singleConflicts = singleConflicts
    
    # Determine if a conflict conflicts with the individualSchedule's current schedule
    # Inputs:
    #   conflict - a conflict object
    # Returns:
    #   bool - true if there is a conflict, false if otherwise
    def doesTimeConflict(self, conflict):

        # First determine if any of the weeklyConflicts conflict with the conflict

        # The days of the week the conflict occurs on
        daysOfConflict = set()
        duplicateStartTime = conflict.startTime.duplicate()
        while duplicateStartTime < conflict.endTime:
            daysOfConflict.add(duplicateStartTime.determineDayOfWeek())
            duplicateStartTime.addTime(0, 0, 1, 0, 0)

        # Check all the determined days of conflict
        for weeklyConflict in self.weeklyConflicts:
            
            # Check to make sure the day of the weeklyConflict matches the dayOfConflict
            dayOfWeeklyConflict = weeklyConflict.determineDayOfWeek()
            if dayOfWeeklyConflict not in daysOfConflict: continue
            
            # Create a TimeStamp for when this weeklyConflict is this week
            weeklyConflictStart = TimeStamp(conflict.year, conflict.month, conflict.day, weeklyConflict.startHour, weeklyConflict.startMinute)
            weeklyConflictEnd = TimeStamp(conflict.year, conflict.month, conflict.day, weeklyConflict.endHour, weeklyConflict.endMinute)
            weeklyConflict = Conflict(str(weeklyConflictStart + " - " + weeklyConflictEnd))

            # Determine if this weekly Conflict conflicts with the conflict
            if Conflict.doConflictsOverlap(weeklyConflict, conflict): return True

        # Check if there are any single conflict conflicts
        for singleConflict in self.singleConflicts:

            if Conflict.doConflictsOverlap(singleConflict, conflict): return True

        # TODO: Check if there are any days off which conflict

        # Return false if there were no conflicts
        return False