# Automatic scheduler for CMU PreCollege Program

from src.individualSchedule import IndividualSchedule
from src.helpers import readNameFile, readFloorFile, readBuildingFile, readWeeklyConflictsFile, readSingleConflictsFile, readWeeklyDutiesFile, readSingleDutiesFile, readDaysOffFile
from src.conflict import Conflict
from src.timeStamp import TimeStamp

# Class for handling all the individual schedules
class Schedule:

    # Constructor
    def __init__(self):
        
        # List of names of those being scheduled
        self.names = readNameFile()
        
        # Set the default attributes
        self.schedules = {}
        self.floors = {}
        self.buildings = {}
        self.weeklyConflicts = {}
        self.singleConflicts = {}
        self.daysOff = {}
        self.schedule = {}

        self.weeklyDuties = {}
        self.singleDuties = {}

        # Load all the data from files
        self.loadSchedules() # Load everyone's schedule
        self.loadFloors() # Load everyone's floor
        self.loadBuildings() # Load everyone's building
        self.loadWeeklyConflicts() # Load everyone's weeklyConflicts
        self.loadSingleConflicts() # Load everyone's singleConflicts
        self.loadDaysOff() # Load everyone's days off

        self.loadWeeklyDuties() # Load the weekly Duties
        self.loadSingleDuties() # Load the single duties

        # Process all the data necessary after it has been loaded in
        self.linkPartners()
    
    # Load the names into the schedule
    def loadSchedules(self):
        
        # Add the initialized schedule to self.schedules
        for name in self.names: self.schedules[name] = IndividualSchedule(name)
    
    # Add the floors to each schedule
    def loadFloors(self):

        # Create the floors dictionary
        self.floors = readFloorFile()

        # Assign all the floors to each schedule
        for name in self.schedules: self.schedules[name].setFloor(self.floors[name])
    
    # Add the buildings to each schedule
    def loadBuildings(self):

        # Create the building dictionary
        self.buildings = readBuildingFile()

        # Assign all the buildings to each schedule
        for name in self.schedules: self.schedules[name].setBuilding(self.buildings[name])
    
    # Add the weekly conflicts to each schedule
    def loadWeeklyConflicts(self):

        # Create the weekly conflicts dictionary
        self.weeklyConflicts = readWeeklyConflictsFile()

        # Assign all the weekly conflicts to each schedule
        for name in self.schedules: self.schedules[name].setWeeklyConflicts(self.weeklyConflicts[name])
    
    # Add the single conflicts to each schedule
    def loadSingleConflicts(self):

        # Create the single conflicts dictionary
        self.singleConflicts = readSingleConflictsFile()

        # Assign all the single conflicts to each schedule
        for name in self.schedules: self.schedules[name].setSingleConflicts(self.singleConflicts[name])
    
    # Add the daysOff to each schedule
    def loadDaysOff(self):

        # Create the daysOff dictionary
        self.daysOff = readDaysOffFile()

        # Assign all the daysOff to each schedule
        for name in self.schedules: self.schedules[name].setDaysOff(self.daysOff[name])

    # Add the weeklyDuties to the main schedule
    def loadWeeklyDuties(self):

        # Attach to self
        self.weeklyDuties = readWeeklyDutiesFile()
    
    # Add the singleDuties to the main schedule
    def loadSingleDuties(self):

        # Attach to self
        self.singleDuties = readSingleDutiesFile()
    
    # Determines which RAs are available during a conflict
    def determineAvailableRAs(self, conflict):

        # Define the output
        availableRAs = set()

        # Loops through all RAs and determine if the RA is available
        for RA in self.schedules:
            if not self.schedules[RA].doesTimeConflict(conflict):
                availableRAs.add(RA)

        # Return the RAs which have been determined to be available
        return availableRAs
    
    # Link each RA to their partner
    def linkPartners(self):

        # For each RA, find the RA or RAs which share a floor
        for RA in self.schedules:
            RASchedule = self.schedules[RA]
            
            # Loop through the RAs again
            for RAPartner in self.schedules:
                if RAPartner == RA: continue
                RAPartnerSchedule = self.schedules[RAPartner]
                
                # Add the partner if both the building and floor match
                if RASchedule.building == RAPartnerSchedule.building and RASchedule.floor == RAPartnerSchedule.floor:
                    RASchedule.partners[RAPartner] = RAPartnerSchedule
    
    # Create a schedule
    def createSchedule(self, startDay, endDay):

        # Will generate a dictionary of every duty and who is available to do those duties
        self.schedule = {}

        # Loop through each day in the schedule
        duplicateStartDay = startDay.duplicate()
        duplicateStartDay.hour = 0
        duplicateStartDay.minute = 0
        endDay.addTime(0, 0, 1, 0, 0)
        while not TimeStamp.isSameDay(duplicateStartDay, endDay):

            # Will generate a dictionary of every duty and who is available to do those duties
            availableRAs = {}

            # Loop through each singleDuty
            for singleDuty in self.singleDuties:

                # If the duty starts on this day, available RAs
                if TimeStamp.isSameDay(self.singleDuties[singleDuty].startTime, duplicateStartDay):
                    availableRAs[singleDuty] = self.determineAvailableRAs(self.singleDuties[singleDuty])

            # Loop through all the weeklyDuties
            for weeklyDuty in self.weeklyDuties:

                # Turn the weeklyDuty into a regular conflict if the weeklyDuty is the correct day of the week
                if duplicateStartDay.determineDayOfWeek() == self.weeklyDuties[weeklyDuty].day:

                    weeklyDutyStart = TimeStamp(duplicateStartDay.year, duplicateStartDay.month, duplicateStartDay.day, self.weeklyDuties[weeklyDuty].startHour, self.weeklyDuties[weeklyDuty].startMinute)
                    weeklyDutyEnd = TimeStamp(duplicateStartDay.year, duplicateStartDay.month, duplicateStartDay.day, self.weeklyDuties[weeklyDuty].endHour, self.weeklyDuties[weeklyDuty].endMinute)
                    generatedWeeklyDuty = Conflict(str(weeklyDutyStart), str(weeklyDutyEnd))
                    
                    # Determine which RAs can perform this duty
                    availableRAs[weeklyDuty] = self.determineAvailableRAs(generatedWeeklyDuty)

            self.schedule[duplicateStartDay.reprDate()] = availableRAs

            duplicateStartDay.addTime(0, 0, 1, 0, 0)
        
        for date in self.schedule:
            print()
            print(date, self.schedule[date])

