"""
Author: Kyle Kolodziej
Created: June 27th, 2021
Last Updated: June 30th, 2021

This file is used to write to an input file called "processInputFile.txt"
that can be used to test the Process Control Board Queue.
"""

import random

file = open("processInputFile.txt", "w") # The file name that is being created
file.write("process_ID, priority\n")
for i in range(50): # The number of processes that are being written to this file
    # For each process...
    # their process ID will be (i+1), thus spanning from 1 to 50
    # their priority will be a random integer between 1 and 10,000
    file.write(str(i+1) + ", " + str(random.randint(1, 10000)) + "\n")
file.close()