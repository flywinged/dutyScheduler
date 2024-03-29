# Automatic scheduler for CMU PreCollege Program

import sys

from src.schedule import Schedule
from src.timeStamp import TimeStamp

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("ERROR: Please input a start date and an end date to schedule")
        sys.exit()
    
    startDate = TimeStamp.createDayFromString(sys.argv[1])
    endDate = TimeStamp.createDayFromString(sys.argv[2])

    # Define the base schedule
    # try:
    schedule = Schedule()
    # except:
    #     print("ERROR: Unable to load schedule for unknown reason. Likely an input file is formatted incorrectly")
    #     sys.exit()
    
    schedule.createSchedule(startDate, endDate)