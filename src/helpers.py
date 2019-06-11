# Automatic scheduler for CMU PreCollege Program

import sys
from os.path import isfile as isFile

from src.conflict import Conflict, RecurringConflict
from src.timeStamp import TimeStamp

# Return all the names written in the names file
def readNameFile():

    # Load the name file so all the necessary files can be created
    nameFile = open("./input/names.txt", "r")

    # Read through each name and accumulate them into a list
    names = []
    for name in nameFile.readlines():
        if name [-1] == "\n": name = name[:-1]
        names.append(name)

    # Close the name file when done
    nameFile.close()

    # Return the accumulated names
    return names

# Return the floors file
def readFloorFile():

    # Load the floors file
    floorFile = open("./input/floors.csv", "r")

    # Create the floors output
    floors = {}
    for line in floorFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(',')

        # Append the data to floors
        floors[splitLine[0]] = splitLine[1]

    # Close the file now that we're done with it
    floorFile.close()

    # Return the accumulated floors
    return floors

# Return the buildings file
def readBuildingFile():

    # Load the buildings file
    buildingFile = open("./input/buildings.csv", "r")

    # Create the buildings output
    buildings = {}
    for line in buildingFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(',')

        # Append the data to buildings
        buildings[splitLine[0]] = splitLine[1]

    # Close the file now that we're done with it
    buildingFile.close()

    # Return the accumulated buildings
    return buildings

# Return the weeklyConflicts file
def readWeeklyConflictsFile():

    # Load the weeklyConflicts file
    weeklyConflictFile = open("./input/weeklyConflicts.csv")

    # Create the weekly conflicts output
    weeklyConflicts = {}
    for line in weeklyConflictFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(",")

        # Create the list of conflicts to attach to the RA
        conflictList = []

        for i in range(1, len(splitLine), 3):

            conflict = splitLine[i]

            # Ensure there is a conflict to write
            if conflict == "": continue

            # Add the conflict to the list of conflicts
            conflictList.append(RecurringConflict(splitLine[i], splitLine[i + 1], splitLine[i + 2]))
        
        # Attach the weekly conflicts to the RA
        weeklyConflicts[splitLine[0]] = conflictList

    # Close the weeklyconflicts file
    weeklyConflictFile.close()

    # Return the generated weekly conflicts
    return weeklyConflicts

# Return the single conflicts file
def readSingleConflictsFile():

    # Load the singleConflicts file
    singleConflictsFile = open("./input/singleConflicts.csv")

    # Create the singleConflicts output
    singleConflicts = {}
    for line in singleConflictsFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(",")

        # Create the list of single conflicts to attach to the RA
        conflictList = []
        for i in range(1, len(splitLine), 4):

            conflict = splitLine[i]

            # Ensure there is a conflict to write
            if conflict == "": continue
            
            # Add the conflict to the list of conflicts
            conflictList.append(Conflict(splitLine[i] + " " + splitLine[i + 1], splitLine[i + 2] + " " + splitLine[i + 3]))
        
        # Attach the single conflicts to the RA
        singleConflicts[splitLine[0]] = conflictList
    
    # Close the singleConflicts file
    singleConflictsFile.close()

    # Return the generated singleConflicts dictionary
    return singleConflicts

# Return the recurring duties file
def readWeeklyDutiesFile():

    # Load the recurringDuties file
    weeklyDutiesFile = open("./input/weeklyDuties.csv")

    # Create the recurring duties output
    weeklyDuties = {}
    dutyTypes = {}
    for line in weeklyDutiesFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(",")

        # Print error message if the splitLine is not in the correct format
        if len(splitLine) != 5:
            print("ERROR: line \"" + line + "\" cannot be parsed as a recurring duty.")
            sys.exit()
        
        # Attach the weekly conflicts to the RA
        weeklyDuties[splitLine[0]] = RecurringConflict(splitLine[2], splitLine[3], splitLine[4])
        if splitLine[1] != "":
            dutyTypes[splitLine[0]] = splitLine[1]

    # Close the weeklyconflicts file
    weeklyDutiesFile.close()

    # Return the generated weekly conflicts
    return weeklyDuties, dutyTypes

# Return the single duties file
def readSingleDutiesFile():

    # Load the recurringDuties file
    singleDutiesFile = open("./input/singleDuties.csv")

    # Create the recurring duties output
    singleDuties = {}
    dutyTypes = {}
    for line in singleDutiesFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(",")

        # Print error message if the splitLine is not in the correct format
        if len(splitLine) != 6:
            print("ERROR: line \"" + line + "\" cannot be parsed as a recurring duty.")
            sys.exit()
        
        # Attach the single Duty to the dictionary of single duties
        singleDuties[splitLine[0]] = Conflict(splitLine[2] + " " + splitLine[3], splitLine[4] + " " + splitLine[5])
        if splitLine[1] != "":
            dutyTypes[splitLine[0]] = splitLine[1]

    # Close the weeklyconflicts file
    singleDutiesFile.close()

    # Return the generated weekly conflicts
    return singleDuties, dutyTypes

# Return the days off file
def readDaysOffFile():

    # Load the daysOff file
    daysOffFile = open("./input/daysOff.csv")

    # Create the daysOff output
    daysOff = {}
    for line in daysOffFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(",")
        
        # Find all the days off
        RADaysOff = []
        for i in range(1, len(splitLine)):
            
            # Make sure there is actualyl a day off here
            if splitLine[i] == "": continue

            dayOffStart = TimeStamp.createTimeFromString(splitLine[i] + " 00:00")
            dayOffEnd = dayOffStart.duplicate()
            dayOffEnd.addTime(0, 0, 1, 0, 0)
            RADaysOff.append(Conflict(str(dayOffStart), str(dayOffEnd)))

        # Attach the RAdaysOff to daysOff
        daysOff[splitLine[0]] = RADaysOff

    # Close the daysOff file
    daysOffFile.close()

    # Return the generated days off
    return daysOff

# Return the dutiesPerformedFile (if it exists)
def readDutiesPerformedFile():
    
    # Create the output
    dutiesPerformed = {}

    # Check if the file exists
    if isFile("./data/dutiesPerformed.csv"):
        
        # Load the file
        dutiesPerformedFile = open("./data/dutiesPerformed.csv")

        # Construct the list of duties
        dutyList = dutiesPerformedFile.readline()[:-1].split(",")[1:]
        
        # For each RA, define which duties they have done
        for line in dutiesPerformedFile.readlines():
            if line[-1] == "\n": line = line[:-1]
            splitLine = line.split(",")

            # Define the RA duties performed
            RADutiesPerformed = {}

            # Attach the count for each duty to the RADutiesPerformed dictionary
            i = 0
            for dutyCount in splitLine[1:]:
                RADutiesPerformed[dutyList[i]] = int(dutyCount)
                i+=1
            
            # Attach the RA duties performed to the dutiesPerformed dictionary
            dutiesPerformed[splitLine[0]] = RADutiesPerformed

        # Close the file
        dutiesPerformedFile.close()
    
    # Return the constructed dutiesPerformed file
    return dutiesPerformed