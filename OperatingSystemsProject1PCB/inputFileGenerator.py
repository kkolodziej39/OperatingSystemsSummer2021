"""
Author: Kyle Kolodziej
Created: June 27th, 2021
Last Updated: June 28th, 2021

This file is used to write to an inputFile that can be used to test the Process Control Board Queue
"""

import random

file = open("processInputFile.txt", "w")
file.write("process_ID, priority\n")
for i in range(50):
    file.write(str(i+1) + ", " + str(random.randint(1, 10000)) + "\n")
file.close()