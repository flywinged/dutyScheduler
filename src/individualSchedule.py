# Automatic scheduler for CMU PreCollege Program

from src.timeStamp import TimeStamp
from src.conflict import Conflict

from copy import deepcopy

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
        self.weeklyConflicts = []
        self.singleConflicts = []
        self.daysOff = []
        self.partners = {}
        self.dutiesPerformed = {}
    
    # Function to duplicate an individual schedule
    def duplicate(self):

        newSchedule = IndividualSchedule("")
        newSchedule.name = deepcopy(self.name)
        newSchedule.floor = deepcopy(self.floor)
        newSchedule.building = deepcopy(self.building)
        newSchedule.weeklyConflicts = deepcopy(self.weeklyConflicts)
        newSchedule.singleConflicts = deepcopy(self.singleConflicts)
        newSchedule.daysOff = deepcopy(self.daysOff)
        newSchedule.partners = deepcopy(self.partners)
        newSchedule.dutiesPerformed = deepcopy(self.dutiesPerformed)

        return newSchedule

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

        printString += "Partners: "
        for partner in self.partners:
            printString += str(partner) + ", "
        printString = printString[:-2] + "\n"

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

        # Determine if the conflict is a building specific duty
        if "On-Duty" in conflict.conflictName or "B" in conflict.flags:
            if self.building not in conflict.conflictName:
                return True

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
            if weeklyConflict.day not in daysOfConflict: continue
            
            # Create a TimeStamp for when this weeklyConflict is this week
            duplicateStartTime = conflict.startTime.duplicate()
            duplicateStartTime.hour = 0
            duplicateStartTime.minute = 0
            while duplicateStartTime <= conflict.endTime:

                # Not the correct day of the week
                if duplicateStartTime.determineDayOfWeek() != weeklyConflict.day:
                    
                    # Increment the time
                    duplicateStartTime.addTime(0, 0, 1, 0, 0)
                    continue
                
                weeklyConflictStart = TimeStamp(duplicateStartTime.year, duplicateStartTime.month, duplicateStartTime.day, weeklyConflict.startHour, weeklyConflict.startMinute)
                weeklyConflictEnd = TimeStamp(duplicateStartTime.year, duplicateStartTime.month, duplicateStartTime.day, weeklyConflict.endHour, weeklyConflict.endMinute)
                generatedWeeklyconflict = Conflict(str(weeklyConflictStart), str(weeklyConflictEnd))

                doesConflictOverlap = Conflict.doConflictsOverlap(generatedWeeklyconflict, conflict)

                if "On-Duty" in conflict.conflictName:
                    if doesConflictOverlap and "D" in weeklyConflict.flags:
                        return True

                    # If no flags, ignore all overlaps if they aren't named. (This means any overlap with non-duties are ignored unless the "D" flag is present)
                    elif doesConflictOverlap and weeklyConflict.conflictName != "No Name":
                        return True
                else:
                    if doesConflictOverlap: return True

                # Increment the time
                duplicateStartTime.addTime(0, 0, 1, 0, 0)

        # Check if there are any single conflict conflicts
        for singleConflict in self.singleConflicts:

            doesConflictOverlap = Conflict.doConflictsOverlap(singleConflict, conflict)
            if "On-Duty" in conflict.conflictName:
                if doesConflictOverlap and "D" in singleConflict.flags:
                    return True

                # If no flags, ignore all overlaps if they aren't named. (This means any overlap with non-duties are ignored unless the "D" flag is present)
                elif doesConflictOverlap and singleConflict.conflictName != "No Name":
                    return True
            
            else:
                if doesConflictOverlap: return True
        
        # TODO: Check if there are any days off which conflict
        for daysOff in self.daysOff:
            if Conflict.doConflictsOverlap(daysOff, conflict): return True
            
        if not isPartner:
            
            # Set the start time for when partners have to be on the same floor
            partnerConflictTimeStart = floorUnattendedStartTime.duplicate()
            partnerConflictTimeStart.year = conflict.startTime.year
            partnerConflictTimeStart.month = conflict.startTime.month
            partnerConflictTimeStart.day = conflict.startTime.day

            # Set the end time from when partners have to be on the same floor
            partnerConflictTimeEnd = partnerConflictTimeStart.duplicate()
            partnerConflictTimeEnd.addTime(0, 0, 0, floorUnattendedLength, 0)

            # Create the conflict time for partners
            partnerTimeConflict = Conflict(str(partnerConflictTimeStart), str(partnerConflictTimeEnd))

            if Conflict.doConflictsOverlap(partnerTimeConflict, conflict):
                for partner in self.partners:
                    if self.partners[partner].doesTimeConflict(conflict, True): return True

        # Return false if there were no conflicts
        return False