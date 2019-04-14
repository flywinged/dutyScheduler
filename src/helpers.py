# Automatic scheduler for CMU PreCollege Program

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
    floorFile = open("./input/floors.txt", "r")

    # Create the floors output
    floors = {}
    for line in floorFile.readlines():
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(':')

        # Append the data to floors
        floors[splitLine[0]] = splitLine[1].replace(" ", "")

    # Close the file now that we're done with it
    floorFile.close()

    # Return the accumulated floors
    return floors

# Return the buildings file
def readBuildingFile():

    # Load the buildings file
    buildingFile = open("./input/buildings.txt", "r")

    # Create the buildings output
    buildings = {}
    for line in buildingFile.readlines():
        if line[-1] == "\n": line = line[:-1]
        splitLine = line.split(':')

        # Append the data to buildings
        buildings[splitLine[0]] = splitLine[1].replace(" ", "")

    # Close the file now that we're done with it
    buildingFile.close()

    # Return the accumulated buildings
    return buildings

# Return the weeklyConflicts file
def readWeeklyConflictsFile():

    pass