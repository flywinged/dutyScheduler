# Automatic scheduler for CMU PreCollege Program

import sys, os

from src.helpers import readNameFile

# Global list of input files
fileNames = ["weeklyConflicts", "singleConflicts", "floors", "buildings", "daysOff"]

# Generate the input files
def generateInputFiles(names):
    
    # Create all the input files
    files = []
    for fileName in fileNames: files.append(open("./input/" + fileName + ".txt", "w"))

    # Make a template for each name
    for name in names:

        # Generate the line that will be written
        line = name + ": "
        
        # Write the line to every file
        for f in files: f.write(line + '\n')

    # Close all the files
    for f in files: f.close()

# Clear input files
def clearInputFiles():
    for fileName in fileNames: os.unlink("./input/" + fileName + ".txt")

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
        
        
