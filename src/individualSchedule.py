# Automatic scheduler for CMU PreCollege Program

from src.timeStamp import TimeStamp
from src.conflict import Conflict

# Use this change what times a floor maybe be unattended
# TODO: Make this loadable by a file
floorUnattendedStartTime = TimeStamp(0, 0, 0, 19, 30)
floorUnattendedLength = 10 # In hours

# Class for handling a schedule for an individual
class IndividualSchedule:

    # Constructor
    def __init__(self, name):
        
        # Define who the schedule is for
        self.name = name

        # Attributes for the individual schedule
        self.floor = None
        self.building = None
        self.weeklyConflicts = {}
        self.singleConflicts = {}
        self.daysOff = []
        self.partners = []
    
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
        printString += "Days Off: " + str(self.daysOff) + "\n"
        printString += "Partners: " + str(self.partners) + "\n"

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
    
    # Set the individuals's days off
    def setDaysOff(self, daysOff):
        self.daysOff = daysOff

    # Determine if a conflict conflicts with the individualSchedule's current schedule
    # Inputs:
    #   conflict - a conflict object
    #   isPartner - if True, keeps the function from recursively calling itself
    # Returns:
    #   bool - true if there is a conflict, false if otherwise
    def doesTimeConflict(self, conflict, isPartner = False):

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
            weeklyConflict = Conflict(str(weeklyConflictStart), str(weeklyConflictEnd))

            # Determine if this weekly Conflict conflicts with the conflict
            if Conflict.doConflictsOverlap(weeklyConflict, conflict): return True

        # Check if there are any single conflict conflicts
        for singleConflict in self.singleConflicts:

            if Conflict.doConflictsOverlap(singleConflict, conflict): return True

        # TODO: Check if there are any days off which conflict
        for daysOff in self.daysOff:

            if Conflict.doConflictsOverlap(daysOff, conflict): return True
            
        # TODO: Make sure no partners have conflicts during this time as well
        if not isPartner:
            
            # Set the start time for when partners have to be on the same floor
            partnerConflictTimeStart = floorUnattendedStartTime.duplicate()
            partnerConflictTimeStart.year = conflict.year
            partnerConflictTimeStart.month = conflict.month
            partnerConflictTimeStart.day = conflict.day

            # Set the end time from when partners have to be on the same floor
            partnerConflictTimeEnd = partnerConflictTimeStart.duplicate()
            partnerConflictTimeEnd.addTime(0, 0, 0, floorUnattendedLength, 0)

            # Create the conflict time for partners
            partnerTimeConflict = Conflict(str(partnerConflictTimeStart), str(partnerConflictTimeEnd))

            # TODO: If the conflict lasts during this time, check if any of the partners have conflict
            # if Conflict.doConflictsOverlap(partnerTimeConflict, conflict):
            #     for partner in self.partners:
            #         if 


        # Return false if there were no conflicts
        return False