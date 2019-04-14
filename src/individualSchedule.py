# Automatic scheduler for CMU PreCollege Program

# Class for handling a schedule for an individual
class IndividualSchedule:

    # Constructor
    def __init__(self, name):
        
        # Define who the schedule is for
        self.name = name
    
    # Print function
    def __repr__(self):

        return "Schedule for: {0}".format(self.name)
