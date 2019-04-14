# Automatic scheduler for CMU PreCollege Program

# Class for handling a schedule for an individual
class IndividualSchedule:

    # Constructor
    def __init__(self, name):
        
        # Define who the schedule is for
        self.name = name
    
    # Print function
    def __repr__(self):

        # Set the output
        printString = ""

        # Header
        printString += "Schedule for: {0}\n".format(self.name)

        # Add the Building and Floor components
        printString += "Building: {0}\n".format(self.building)
        printString += "Floor: {0}\n".format(self.floor)

        return printString
    
    # Set the individual's floor
    def setFloor(self, floor):
        self.floor = floor
    
    # Set the individual's building
    def setBuilding(self, building):
        self.building = building
