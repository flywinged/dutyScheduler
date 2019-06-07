# Automatic scheduler for CMU PreCollege Program

import sys, os

from src.helpers import readNameFile

# Global list of input files
fileNames = ["weeklyConflicts", "singleConflicts", "floors", "buildings", "daysOff", "weeklyDuties", "singleDuties"]

# Generate the input files
def generateInputFiles(names):
    
    # Create all the input files
    files = []
    for fileName in fileNames: files.append(open("./input/" + fileName + ".csv", "w"))

    # Create the format guide for each file
    # weeklyConflicts guide
    files[0].write("[RA Name],[Day 1],[Start Time 1],[End Time 1],[Day 2],[Start Time 2],[Start Time 2],...[Day N],[Start Time N],[End Time N]\n")

    # singleConflicts Guide
    files[1].write("[RA Name],[Start Date 1],[Start Time 1],[End Date 1],[End Time 1],...[Start Date N],[Start Time N],[End Date N],[End Time N]\n")

    # floors guide
    files[2].write("[RA Name],[Floor]\n")

    # buildings guide
    files[3].write("[RA Name],[Building]\n")

    # daysOff guide
    files[4].write("[RA Name],[Date 1],[Date 2],[Date N]\n")

    # recurringDuties guide
    files[5].write("[Duty Name],[Day],[Start Time],[End Time]\n")

    # singleDuties guide
    files[6].write("[Duty Name],[Start Date],[Start Time],[End Date],[End Time]\n")

    # Make a template for each name
    for name in names[:5]:

        # Generate the line that will be written
        line = name + ","
        
        # Write the line to every file
        for f in files: f.write(line + '\n')

    # Close all the files
    for f in files: f.close()

# Clear input files
def clearInputFiles():
    for fileName in fileNames: os.unlink("./input/" + fileName + ".csv")

# Initialize all the input files for the user
if __name__ == "__main__":
    
    # No arguments. Just initialize
    if len(sys.argv) == 1:
        
        # Read all the names from the name file
        names = readNameFile()

        # Generate all the input files
        generateInputFiles(names)
    
    # Clear all the input files
    elif sys.argv[1] == "clean":
        if input("Are you sure you want to clean the inputs? (type yes and press enter to clear) ") == "yes":
            clearInputFiles()
        
        
