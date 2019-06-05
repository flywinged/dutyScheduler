# Automatic scheduler for CMU PreCollege Program

# Class for handling a schedule for an individual
class IndividualSchedule:

    # Constructor
    def __init__(self, name):
        
        # Define who the schedule is for
        self.name = name

        # Attributes for the individual schedule
        self.floor = None
        self.building = None
        self.weeklyConflicts = None
        self.singleConflicts = None
    
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