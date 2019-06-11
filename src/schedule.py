# Automatic scheduler for CMU PreCollege Program

from src.individualSchedule import IndividualSchedule
from src.helpers import readNameFile, readFloorFile, readBuildingFile, readWeeklyConflictsFile, readSingleConflictsFile, readWeeklyDutiesFile, readSingleDutiesFile, readDaysOffFile, readDutiesPerformedFile
from src.conflict import Conflict
from src.timeStamp import TimeStamp
from copy import deepcopy

# Class for handling all the individual schedules
class Schedule:

    # Constructor
    def __init__(self, loadFiles = True):
        
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
        self.dutiesPerformed = {}

        self.weeklyDuties = {}
        self.singleDuties = {}
        self.dutyTypes = {}

        if loadFiles:

            # Load all the data from files
            self.loadSchedules() # Load everyone's schedule
            self.loadFloors() # Load everyone's floor
            self.loadBuildings() # Load everyone's building
            self.loadWeeklyConflicts() # Load everyone's weeklyConflicts
            self.loadSingleConflicts() # Load everyone's singleConflicts
            self.loadDaysOff() # Load everyone's days off
            self.loadDutiesPerformed() # Load all the previously completed duties

            self.loadWeeklyDuties() # Load the weekly Duties
            self.loadSingleDuties() # Load the single duties

            # Process all the data necessary after it has been loaded in
            self.linkPartners()
    
    # Duplication function
    def duplicate(self):

        # Create the new schedule
        newSchedule = Schedule(loadFiles = False)

        # Copy over all the data
        newSchedule.schedules = deepcopy(self.schedules)
        newSchedule.floors = deepcopy(self.floors)
        newSchedule.buildings = deepcopy(self.buildings)
        newSchedule.weeklyConflicts = deepcopy(self.weeklyConflicts)
        newSchedule.singleConflicts = deepcopy(self.singleConflicts)
        newSchedule.daysOff = deepcopy(self.daysOff)
        newSchedule.schedule = deepcopy(self.schedule)
        newSchedule.dutiesPerformed = deepcopy(self.dutiesPerformed)

        newSchedule.weeklyDuties = deepcopy(self.weeklyDuties)
        newSchedule.singleDuties = deepcopy(self.singleDuties)
        newSchedule.dutyTypes = deepcopy(self.dutyTypes)

        # Return the new schedule
        return newSchedule
    
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
        self.weeklyDuties, weeklyDutyTypes = readWeeklyDutiesFile()
        for duty in weeklyDutyTypes:
            self.dutyTypes[duty] = weeklyDutyTypes[duty]
    
    # Add the singleDuties to the main schedule
    def loadSingleDuties(self):

        # Attach to self
        self.singleDuties, singleDutyTypes = readSingleDutiesFile()
        for duty in singleDutyTypes:
            self.dutyTypes[duty] = singleDutyTypes[duty]
    
    # Load the dutiesPerformed file and add them to the main schedule
    def loadDutiesPerformed(self):
        
        # Read the dutiesPerformed file if it exists
        dutiesPerformed = readDutiesPerformedFile()

        # Assign each RA the appropriate dutiesPerformed
        for name in self.schedules:

            if name in dutiesPerformed:
                self.dutiesPerformed[name] = dutiesPerformed[name]
                self.schedules[name].dutiesPerformed = dutiesPerformed[name]
            else:
                self.dutiesPerformed[name] = {}
                self.schedules[name].dutiesPerformed = {}

    # Saves the current number of duties performed by each RA
    def saveDutiesPerformed(self):

        # Open the outputFile
        dutiesPerformedFile = open("./data/dutiesPerformed.csv", "w")

        # Write the header line
        headerLine = "Duty Types,"
        orderedDuties = []
        for duty in self.dutyTypes:
            if self.dutyTypes[duty] not in orderedDuties:
                headerLine += self.dutyTypes[duty] + ","
                orderedDuties.append(self.dutyTypes[duty])
        headerLine = headerLine[:-1] + "\n"
        dutiesPerformedFile.write(headerLine)

        # Write the performed duties by each RA
        for RA in self.schedules:
            
            # Start the dutiesPerformedLine
            dutiesPerformedLine = RA

            # Loop through the duties in the same order
            for duty in orderedDuties:
                
                # If the RA hasn't performed this duty before, record a zero
                if duty not in self.dutiesPerformed[RA]:
                    dutiesPerformedLine += ",0"
                
                # Otherwise, write the number of times the RA has performed the duty
                else:
                    dutiesPerformedLine += "," + str(self.dutiesPerformed[RA][duty])
            
            # Add the end of the line to the dutiesPerformedLine and write it to the output file
            dutiesPerformedLine += "\n"
            dutiesPerformedFile.write(dutiesPerformedLine)

        # Close the outputFile
        dutiesPerformedFile.close()

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
    
    # Creates a list of available RAs for all duties on a certain day
    def createAvailableRAsForDay(self, day):

        # Will generate a dictionary of every duty and who is available to do those duties
        availableRAs = {}

        # Loop through each singleDuty
        for singleDuty in self.singleDuties:

            # If the duty starts on this day, available RAs
            if TimeStamp.isSameDay(self.singleDuties[singleDuty].startTime, day):
                availableRAs[singleDuty] = {
                    "conflict": self.singleDuties[singleDuty],
                    "set": self.determineAvailableRAs(self.singleDuties[singleDuty])
                }

        # Loop through all the weeklyDuties
        for weeklyDuty in self.weeklyDuties:

            # Turn the weeklyDuty into a regular conflict if the weeklyDuty is the correct day of the week
            if day.determineDayOfWeek() == self.weeklyDuties[weeklyDuty].day:

                weeklyDutyStart = TimeStamp(day.year, day.month, day.day, self.weeklyDuties[weeklyDuty].startHour, self.weeklyDuties[weeklyDuty].startMinute)
                weeklyDutyEnd = TimeStamp(day.year, day.month, day.day, self.weeklyDuties[weeklyDuty].endHour, self.weeklyDuties[weeklyDuty].endMinute)
                generatedWeeklyDuty = Conflict(str(weeklyDutyStart), str(weeklyDutyEnd))
                
                # Determine which RAs can perform this duty
                availableRAs[weeklyDuty] = {
                    "conflict": generatedWeeklyDuty,
                    "set": self.determineAvailableRAs(generatedWeeklyDuty)
                }

        return availableRAs
    
    # Creates available RAs through a range of dates
    def createAvailableRAsForRange(self, startDay, endDay):

        # Will generate a dictionary of every duty and who is available to do those duties
        availableRAs = {}

        # Loop through each day in the schedule
        duplicateStartDay = startDay.duplicate()
        duplicateStartDay.hour = 0
        duplicateStartDay.minute = 0
        endDay.addTime(0, 0, 1, 0, 0)
        while not TimeStamp.isSameDay(duplicateStartDay, endDay):

            # Create the available RAs for each duty on this day
            availableRAs[duplicateStartDay.reprDate()] = self.createAvailableRAsForDay(duplicateStartDay)
            duplicateStartDay.addTime(0, 0, 1, 0, 0)
        
        return availableRAs

    # Determines and assigns an RA for a given duty
    def determineAndAssignRA(self, conflict, RASet):

        pass

    # Create a schedule
    def createSchedule(self, startDay, endDay):

        # Determine the available RAs in this date range
        availableRAs = self.createAvailableRAsForRange(startDay, endDay)
        
        # Now we need to choose an RA for each duty
        self.schedule = {}

        # Save the state before trying anything
        savedState = self.duplicate()
        savedAvailableRAs = deepcopy(availableRAs)

        # Loop through each date and choose an RA to perform each duty
        for date in availableRAs:
            print()
            print(date, availableRAs[date])

