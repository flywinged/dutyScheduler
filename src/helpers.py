# Automatic scheduler for CMU PreCollege Program

from src.conflict import Conflict, RecurringConflict

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
    for line in weeklyDutiesFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(",")

        # Print error message if the splitLine is not in the correct format
        if len(splitLine) != 4:
            print("ERROR: line \"" + line + "\" cannot be parsed as a recurring duty.")
        
        # Attach the weekly conflicts to the RA
        weeklyDuties[splitLine[0]] = RecurringConflict(splitLine[1], splitLine[2], splitLine[3])

    # Close the weeklyconflicts file
    weeklyDutiesFile.close()

    # Return the generated weekly conflicts
    return weeklyDuties

# Return the single duties file
def readSingleDutiesFile():

    # Load the recurringDuties file
    singleDutiesFile = open("./input/singleDuties.csv")

    # Create the recurring duties output
    singleDuties = {}
    for line in singleDutiesFile.readlines()[1:]:
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(",")

        # Print error message if the splitLine is not in the correct format
        if len(splitLine) != 5:
            print("ERROR: line \"" + line + "\" cannot be parsed as a recurring duty.")
        
        # Attach the weekly conflicts to the RA
        singleDuties[splitLine[0]] = Conflict(splitLine[1] + " " + splitLine[2], splitLine[3] + " " + splitLine[4])

    # Close the weeklyconflicts file
    singleDutiesFile.close()

    # Return the generated weekly conflicts
    return singleDuties