# Automatic scheduler for CMU PreCollege Program

import time, datetime

# Class to handle scheduling conflicts
class Conflict:

    # Constructor
    def __init__(self, text):

        # print(time.struct_time([2019]))
        print(time.localtime())
        print(text)

Conflict("Monday(03:00-21:54)")