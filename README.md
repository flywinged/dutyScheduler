# Requirements
Must have python3 installed on machine

# Running the Program
First, run the command 
```
python3 init.py
```

By default, all weekly conflicts and single conflicts allow for an RA to be on duty during that time.
If you would like to disallow an RA from being on duty during that day, place a capital "D" directly after the start time. If you would like a duty on be building specific, place a capital "B" directly after. The conflict must also have the name of the building in its name if the "B" flag is used.
examples below.
```
    WeeklyConflict: Thursday,10:30D,03:00
    SingleConflict: 07/10/2019,11:00D,07/10/2019,12:10,07/13/2019
    WeeklyDuty: Thursday,10:30DB,03:00
    SingleDuty: 07/10/2019,11:00D,07/10/2019,12:10,07/13/2019
```
