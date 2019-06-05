# Automatic scheduler for CMU PreCollege Program

from src.individualSchedule import IndividualSchedule
from src.helpers import readNameFile, readFloorFile, readBuildingFile

# Class for handling all the individual schedules
class Schedule:

    # Constructor
    def __init__(self):
        
        # List of names of those being scheduled
        self.names = readNameFile()
        
        # Set the attributes
        self.schedules = {}
        self.floors = {}
        self.buildings = {}

        self.loadSchedules() # Load everyone's schedule
        self.loadFloors() # Load everyone's floor
        self.loadBuildings() # Load everyone's building

        print(self.schedules)
    
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
        