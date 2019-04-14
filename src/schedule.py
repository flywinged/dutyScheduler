# Automatic scheduler for CMU PreCollege Program

from src.individualSchedule import IndividualSchedule

# Class for handling all the individual schedules
class Schedule:

    # Constructor
    def __init__(self):
        
        # Load everyone's names
        self.schedules = self.loadSchedules()

        print(self.schedules)
    
    # Load the names into the schedule
    def loadSchedules(self):
        
        # Define the function output
        schedules = []

        # Open the names.csv file
        nameFile = open("./data/names.txt")

        # Read all the names in the file and append them to schedules
        for name in nameFile.readlines():

            if name[-1] == "\n": name = name[:-1]
            schedules.append(IndividualSchedule(name))

        # Close the name file now that we're done
        nameFile.close()

        # Return extracted schedules
        return schedules