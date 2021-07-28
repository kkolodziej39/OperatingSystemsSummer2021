"""
Author: Kyle Kolodziej
Created: July 12th, 2021
Last Updated: July 27th, 2021
"""
import operator
import sys
import numpy as np
from tabulate import tabulate
import matplotlib.pyplot as plt

"""
Shortest Job First algo
-Waiting process with the smallest execution time to execute next
- Non-preemptive algorithm
- Greedy algo --> shortest min avg wait time
- Starvation with shorter processes coming in

1) Into array
2) Sort array by their arrival time
3) Begin execution (arrival time of 0 process)
    - Counter that keeps track of curr time
4) Loop through array, checking to see the shortest burst time of the processes that are available at this curr time (by checking the curr time var)
    - In case of a tie give the process with the higher priority execution
5) Repeat step 4 until array is empty

Adjust Non Preemptive Priority to go by Priority rather than burst time

"""

class Process:
    """
    A class that will be used to represent a Process

    ...

    Attributes
    ----------
    processID : string
        a string that contains the Process ID of the Process (can be a mix of letters, numbers, and symbols)
    arrivalTime: integer
        the time that the Process arrives
    burstTime: integer
        the time that the Process takes to execute
    priority : integer
        the priority value of the Process (1 being the highest priority...bigger numbers lower priority)
    next: Process
        each Process will have a pointer to the next Process in the Process Control Block
    """
    def __init__(self, processID, arrivalTime, burstTime, priority=None, waitTime=None, turnaroundTime=None):
        """
        Parameters
        ----------
        :param processID: string
            a string that contains the Process ID of the Process (can be a mix of letters, numbers, and symbols)
        :param arrivalTime: integer
            the time that the Process arrives
        :param burstTime: integer
            the time that the Process takes to execute
        :param priority: int, optional
            the priority value of the Process (1 being the highest priority...bigger numbers lower priority)
            the default values is -1 (it doesn't have a priority)
        """
        self.processID = processID
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        if priority is None:
            self.priority = -1
        else:
            self.priority = priority
        if waitTime is None:
            self.waitTime = -1
        else:
            self.waitTime = waitTime
        if turnaroundTime is None:
            self.turnaroundTime = -1
        else:
            self.turnaroundTime = turnaroundTime
        self.next = None

    def setWaitTime(self, waitTime):
        if waitTime is None:
            pass
        else:
            self.waitTime = waitTime

    def setTurnaroundTime(self, turnaroundTime):
        if turnaroundTime is None:
            pass
        else:
            self.turnaroundTime = turnaroundTime

    def getBurstTime(self):
        return self.burstTime

def runShortestJobFirst(processArray):
    numProcesses = len(processArray)
    returnArray = []
    currTime = 0
    totalWaitTime = 0
    totalTurnaroundTime = 0

    #first process here
    firstProcess = processArray[0]
    processArray.remove(firstProcess)
    firstProcess.setWaitTime(0)
    firstProcess.setTurnaroundTime(firstProcess.burstTime)
    totalTurnaroundTime += firstProcess.burstTime
    returnArray.append(firstProcess)
    currTime += firstProcess.burstTime
    while len(processArray) > 1:
        #do stuff
        index = 0
        currPriority = processArray[0].priority
        lowBurst = processArray[0].burstTime

        for i in range(1, len(processArray)):
            if processArray[i].arrivalTime <= currTime:
                if processArray[i].burstTime < lowBurst or (processArray[i].burstTime == lowBurst and processArray[i].priority < currPriority) :
                    # update process
                    index = i
                    currPriority = processArray[i].priority
                    lowBurst = processArray[i].burstTime
            else:
                break
        # index contains the process we want
        newProcess = processArray[index]
        newWaitTime = currTime - newProcess.arrivalTime  # Calculate this Process' wait time
        newProcess.setWaitTime(newWaitTime)
        totalWaitTime += newWaitTime
        currTime += newProcess.burstTime
        newTurnaroundTime = currTime - newProcess.arrivalTime  # Calculate this Process' turnaround time
        totalTurnaroundTime += newTurnaroundTime
        newProcess.setTurnaroundTime(newTurnaroundTime)
        returnArray.append(newProcess)
        del processArray[index]

    newProcess = processArray[0]
    newWaitTime = currTime - newProcess.arrivalTime  # Calculate this Process' wait time
    newProcess.setWaitTime(newWaitTime)
    totalWaitTime += newWaitTime
    currTime += newProcess.burstTime
    newTurnaroundTime = currTime - newProcess.arrivalTime  # Calculate this Process' turnaround time
    newProcess.setTurnaroundTime(newTurnaroundTime)
    totalTurnaroundTime += newTurnaroundTime
    returnArray.append(newProcess)

    # An array that will contain the total time, average wait time, and average turnaround time of this algo
    algoStats = []
    algoStats.append(currTime)
    averageWaitTime = totalWaitTime * 1.0 / numProcesses
    algoStats.append(averageWaitTime)
    averageTurnaroundTime = totalTurnaroundTime * 1.0 / numProcesses
    algoStats.append(averageTurnaroundTime)

    return returnArray, algoStats

def runHighestPriority(processArray):
    numProcesses = len(processArray)
    returnArray = []
    currTime = 0
    totalWaitTime = 0
    totalTurnaroundTime = 0

    #first process here
    firstProcess = processArray[0]
    processArray.remove(firstProcess)
    firstProcess.setWaitTime(0)
    firstProcess.setTurnaroundTime(firstProcess.burstTime)
    totalTurnaroundTime += firstProcess.burstTime
    returnArray.append(firstProcess)
    currTime += firstProcess.burstTime
    while len(processArray) > 1:
        #do stuff
        index = 0
        bestPriority = processArray[0].priority
        currBurst = processArray[0].burstTime

        for i in range(1, len(processArray)):
            if processArray[i].arrivalTime <= currTime:
                if processArray[i].priority < bestPriority or (processArray[i].priority == bestPriority and processArray[i].burstTime < currBurst) :
                    # update process
                    index = i
                    bestPriority = processArray[i].priority
                    currBurst = processArray[i].burstTime
            else:
                break
        # index contains the process we want
        newProcess = processArray[index]
        newWaitTime = currTime - newProcess.arrivalTime # Calculate this Process' wait time
        newProcess.setWaitTime(newWaitTime)
        totalWaitTime += newWaitTime
        currTime += newProcess.burstTime
        newTurnaroundTime = currTime - newProcess.arrivalTime # Calculate this Process' turnaround time
        newProcess.setTurnaroundTime(newTurnaroundTime)
        totalTurnaroundTime += newTurnaroundTime
        returnArray.append(newProcess)
        del processArray[index]

    newProcess = processArray[0]
    newWaitTime = currTime - newProcess.arrivalTime  # Calculate this Process' wait time
    newProcess.setWaitTime(newWaitTime)
    totalWaitTime += newWaitTime
    currTime += newProcess.burstTime
    newTurnaroundTime = currTime - newProcess.arrivalTime  # Calculate this Process' turnaround time
    newProcess.setTurnaroundTime(newTurnaroundTime)
    totalTurnaroundTime += newTurnaroundTime
    returnArray.append(newProcess)

    # An array that will contain the total time, average wait time, and average turnaround time of this algo
    algoStats = []
    algoStats.append(currTime)
    averageWaitTime = totalWaitTime * 1.0 / numProcesses
    algoStats.append(averageWaitTime)
    averageTurnaroundTime = totalTurnaroundTime * 1.0 / numProcesses
    algoStats.append(averageTurnaroundTime)

    return returnArray, algoStats

def printStatistics(statsArray):
    print("Total Execution Time: ", statsArray[0])
    print("Average Wait Time: ", statsArray[1])
    print("Average Turnaround Time: ", statsArray[2])
    print("\n----------------------------------------------------------------------------------------------\n")

def calculateStats():
    # Need to run the different file size for both SJF and NPP Scheduling Algorithms
    fileNames = ["sample_input_scheduling_part2.txt", "processInputFile10.txt", "processInputFile25.txt",
                 "processInputFile50.txt", "processInputFile100.txt"]
    allNumbersForSJF = []
    allNumbersForNPP = []

    for file in fileNames:
        statsArraySJF = executeInputFile(file, "sjf", False)
        allNumbersForSJF.append(statsArraySJF)

        statsArrayNPP = executeInputFile(file, "npp", False)
        allNumbersForNPP.append(statsArrayNPP)

    return allNumbersForSJF, allNumbersForNPP

def generateCharts():
    sjfArray, nppArray = calculateStats()
    numFiles = [5,10,25,50,100]
    sjfTime = []
    sjfWait = []
    sjfTurnaround = []
    nppTime = []
    nppWait = []
    nppTurnaround = []

    # total time, wait time, turn around time
    for i in range(len(sjfArray)):
        sjfTime.append(sjfArray[i][0])
        sjfWait.append(sjfArray[i][1])
        sjfTurnaround.append(sjfArray[i][2])

        nppTime.append(nppArray[i][0])
        nppWait.append(nppArray[i][1])
        nppTurnaround.append(nppArray[i][2])


    X_axis = np.arange(len(numFiles))

    plt.bar(X_axis - 0.2, sjfTime, 0.4, label='Shortest Job First')
    plt.bar(X_axis + 0.2, nppTime, 0.4, label='Non Preemptive Priority')
    plt.xticks(X_axis, numFiles)
    plt.xlabel("Number of Files")
    plt.ylabel("Time")
    plt.title("Shortest Job First vs Non Preemptive Priority Total Times")
    plt.legend()
    plt.savefig("Shortest Job First vs Non Preemptive Priority - Total Time.png")
    plt.show()

    plt.bar(X_axis - 0.2, sjfWait, 0.4, label='Shortest Job First')
    plt.bar(X_axis + 0.2, nppWait, 0.4, label='Non Preemptive Priority')
    plt.xticks(X_axis, numFiles)
    plt.xlabel("Number of Files")
    plt.ylabel("Time")
    plt.title("Shortest Job First vs Non Preemptive Priority Average Wait Times")
    plt.legend()
    plt.savefig("Shortest Job First vs Non Preemptive Priority - Average Wait Time.png")
    plt.show()

    plt.bar(X_axis - 0.2, sjfTurnaround, 0.4, label='Shortest Job First')
    plt.bar(X_axis + 0.2, nppTurnaround, 0.4, label='Non Preemptive Priority')
    plt.xticks(X_axis, numFiles)
    plt.xlabel("Number of Files")
    plt.ylabel("Time")
    plt.legend()
    plt.title("Shortest Job First vs Non Preemptive Priority Average Turnaround Times")
    plt.savefig("Shortest Job First vs Non Preemptive Priority - Average Turnaround Time.png")
    plt.show()


def executeInputFile(inputFileName, algorithm, toPrint=True):
    processArray = []

    if toPrint:
        print("\n----------------------------------------------------------------------------------------------")
        print("Input file being executed: " + inputFileName)

    if algorithm == "sjf":
        # Shortest Job First Algo
        if toPrint:
            print("Algorithm: Shortest Job First Scheduling")
            print("----------------------------------------------------------------------------------------------\n")

        fileOpened = open(inputFileName, "r")
        for line in fileOpened:
            #process input file
            if line.startswith("process") or line.startswith("Process"):
                pass
            else:
                splittedString = line.split(',')
                processID = splittedString[0]
                arrivalTime = int(splittedString[1])
                burstTime = int(splittedString[2])
                priority = splittedString[3]
                newProcess = Process(processID, arrivalTime, burstTime, priority)
                processArray.append(newProcess)
        # Done reading through the file
        # Time to sort the array of processes based on their arrival time
        processArray.sort(key=operator.attrgetter('arrivalTime'))

        orderedArray, statsArray = runShortestJobFirst(processArray)

        if toPrint:
            columns = ('Process ID', 'Arrival Time', 'Burst Time', 'Priority', 'Wait Time', 'Turnaround Time')
            n_rows = len(orderedArray)
            cell_text = []
            for row in range(n_rows):
                processInfo = [orderedArray[row].processID, orderedArray[row].arrivalTime, orderedArray[row].burstTime, orderedArray[row].priority, orderedArray[row].waitTime, orderedArray[row].turnaroundTime]
                cell_text.append(processInfo)


            print(tabulate(cell_text, headers=columns, tablefmt="grid"))
            printStatistics(statsArray)
        else:
            return statsArray

    else:
        #Non preemptive
        if toPrint:
            print("Algorithm: Non-Preemptive Priority Scheduling")
            print("----------------------------------------------------------------------------------------------\n")

        fileOpened = open(inputFileName, "r")
        for line in fileOpened:
            # process input file
            if line.startswith("process") or line.startswith("Process"):
                pass
            else:
                splittedString = line.split(',')
                processID = splittedString[0]
                arrivalTime = int(splittedString[1])
                burstTime = int(splittedString[2])
                priority = splittedString[3]
                newProcess = Process(processID, arrivalTime, burstTime, priority)
                processArray.append(newProcess)
        # Done reading through the file
        # Time to sort the array of processes based on their priority
        processArray.sort(key=operator.attrgetter('arrivalTime'))
        orderedArray, statsArray = runHighestPriority(processArray)

        if toPrint:
            columns = ('Process ID', 'Arrival Time', 'Burst Time', 'Priority', 'Wait Time', 'Turnaround Time')
            n_rows = len(orderedArray)
            cell_text = []
            for row in range(n_rows):
                processInfo = [orderedArray[row].processID, orderedArray[row].arrivalTime, orderedArray[row].burstTime,
                               orderedArray[row].priority, orderedArray[row].waitTime, orderedArray[row].turnaroundTime]
                cell_text.append(processInfo)
            print(tabulate(cell_text, headers=columns, tablefmt="grid"))
            printStatistics(statsArray)
        else:
            return statsArray
    return 0

print("----------------------------------------------------------------------------------------------------------------------\n")
print("Welcome to Kyle Kolodziej's Operating System's Project #2: Shortest Job First and Non-Preemptive Priority Scheduling!\n")
print("----------------------------------------------------------------------------------------------------------------------")

userInput = 0
while userInput != 4:
    print("-----------------------------------------------------------------------------------------------------")
    print("Would you like to...")
    print("\t1) Read through an Input file using Shortest Job First Scheduling")
    print("\t2) Read through an Input file using Non-Preemptive Priority Scheduling")
    print("\t3) Generate Charts for both Shortest Job First Scheduling and Non-Preemptive Priority Scheduling")
    print("\t4) Exit")
    print("-----------------------------------------------------------------------------------------------------\n")
    try:
        userInput = int(input("Please input your option (1-4): "))
        if 1 <= userInput <= 4:
            if userInput == 1:
                # Shortest Job First Algo
                shortestJobFirstSelection = 0
                while shortestJobFirstSelection != 6 and shortestJobFirstSelection != 7:
                    print("\nPlease select the size of the Input File you would like to execute...")
                    print("\t1) 5 Processes (the class sample file)")
                    print("\t2) 10 Processes (randomly generated file)")
                    print("\t3) 25 Processes (randomly generated file)")
                    print("\t4) 50 Processes (randomly generated file)")
                    print("\t5) 100 Processes (randomly generated file)")
                    print("\t6) Go Back to the Main Menu")
                    print("\t7) Exit the Program\n")
                    try:
                        shortestJobFirstSelection = int(input("Please input your option (1-7): "))
                        if 1 <= shortestJobFirstSelection <= 7:
                            if shortestJobFirstSelection == 1:
                                # Run the class sample file
                                executeInputFile("sample_input_scheduling_part2.txt", "sjf")
                            elif shortestJobFirstSelection == 2:
                                # Run the file with 10 processes
                                executeInputFile("processInputFile10.txt", "sjf")
                            elif shortestJobFirstSelection == 3:
                                # Run the file with 25 processes
                                executeInputFile("processInputFile25.txt", "sjf")
                            elif shortestJobFirstSelection == 4:
                                # Run the file with 50 processes
                                executeInputFile("processInputFile50.txt", "sjf")
                            elif shortestJobFirstSelection == 5:
                                # Run the file with 100 processes
                                executeInputFile("processInputFile100.txt", "sjf")
                            elif shortestJobFirstSelection == 6:
                                # Go back to the main menu
                                print("Returning to the main menu...\n")
                                userInput = 0
                                break
                            else:
                                # Exit the program
                                userInput = 4
                                print("Exiting the program...")
                                print(
                                    "\n-----------------------------------------------------------------------------------------------------\n")
                                print("Thank you for using Kyle Kolodziej's Operating Systems Project Part 2! Goodbye!")
                                print(
                                    "\n-----------------------------------------------------------------------------------------------------\n")
                                break
                        else:
                            raise Exception
                    except:
                        print("\nError, invalid option! Please input a valid option!")
            elif userInput == 2:
                # Non Preemptive Priority Scheduling
                prioriotySchedulingSelection = 0
                while prioriotySchedulingSelection != 6 and prioriotySchedulingSelection != 7:
                    print("\nPlease select the size of the Input File you would like to execute...")
                    print("\t1) 5 Processes (the class sample file)")
                    print("\t2) 10 Processes (randomly generated file)")
                    print("\t3) 25 Processes (randomly generated file)")
                    print("\t4) 50 Processes (randomly generated file)")
                    print("\t5) 100 Processes (randomly generated file)")
                    print("\t6) Go Back to the Main Menu")
                    print("\t7) Exit the Program\n")
                    try:
                        prioriotySchedulingSelection = int(input("Please input your option (1-7): "))
                        if 1 <= prioriotySchedulingSelection <= 7:
                            if prioriotySchedulingSelection == 1:
                                # Run the class sample file
                                executeInputFile("sample_input_scheduling_part2.txt", "npp")
                            elif prioriotySchedulingSelection == 2:
                                # Run the file with 10 processes
                                executeInputFile("processInputFile10.txt", "npp")
                            elif prioriotySchedulingSelection == 3:
                                # Run the file with 25 processes
                                executeInputFile("processInputFile25.txt", "npp")
                            elif prioriotySchedulingSelection == 4:
                                # Run the file with 50 processes
                                executeInputFile("processInputFile50.txt", "npp")
                            elif prioriotySchedulingSelection == 5:
                                # Run the file with 100 processes
                                executeInputFile("processInputFile100.txt", "npp")
                            elif prioriotySchedulingSelection == 6:
                                # Go back to the main menu
                                print("Returning to the main menu...\n")
                                userInput = 0
                                break
                            else:
                                # Exit the program
                                userInput = 4
                                print("Exiting the program...")
                                print(
                                    "\n-----------------------------------------------------------------------------------------------------\n")
                                print("Thank you for using Kyle Kolodziej's Operating Systems Project Part 2! Goodbye!")
                                print(
                                    "\n-----------------------------------------------------------------------------------------------------\n")
                                break
                        else:
                            raise Exception
                    except:
                        print("\nError, invalid option! Please input a valid option!")
            elif userInput == 3:
                print("Generating Charts...\n")
                generateCharts()
                print("Charts Completed...")
                print(
                    "----------------------------------------------------------------------------------------------\n")
            else:
                print("\n-----------------------------------------------------------------------------------------------------\n")
                print("Thank you for using Kyle Kolodziej's Operating Systems Project Part 2! Goodbye!")
                print(
                    "\n-----------------------------------------------------------------------------------------------------\n")
                break
        else:
            raise Exception
    except:
        print("\nError, invalid option! Please input a valid option!")
