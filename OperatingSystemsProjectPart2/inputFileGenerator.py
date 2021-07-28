"""
Author: Kyle Kolodziej
Created: July 12th, 2021
Last Updated: July 25th, 2021

This file is used to write to input files called that can be used to test the algorithms.
This file will create four different input files that contain either 10, 25, 50, or 100 Processes in it.
Each Process will contain a process ID, arrival time, burst time, and priority
"""

import random

priorities = [1,2,3,4] # The different priority values that will be used for Processes
numberOfProcesses = [10, 25, 50, 100] # The number of Processes that will be in the different input files

for i in range(len(numberOfProcesses)):
    fileName = "processInputFile" + str(numberOfProcesses[i]) + ".txt"
    file = open(fileName, "w")  # The file name that is being created
    file.write("process_ID, arrival_time, burst_time, priority\n")
    processWithArrivalTimeOfZero = random.randint(0, numberOfProcesses[i] - 1)
    for k in range(numberOfProcesses[i]):
        # For each process...
        # their process ID will be (i+1), thus spanning from 1 to the number of Processes for that input file
        # their arrival time will be either a random integer between 1 and the number of Processes for that input file
        #   except for one of the Processes which will contain an arrival time of 0
        # their burst time will be a random integer between 1 and 10
        # their priority will be a random integer between 1 and 4
        if k == processWithArrivalTimeOfZero:
            # This Process will have an arrival time of 0
            file.write(str(k + 1) + ", " + "0" + ", " + str(random.randint(1, 10)) + ", " + str(priorities[random.randint(0, 3)]) + "\n")
        else:
            file.write(str(k + 1) + ", " + str(random.randint(1, numberOfProcesses[i])) + ", " + str(random.randint(1, 10)) + ", " + str(priorities[random.randint(0, 3)]) + "\n")
    file.close()
