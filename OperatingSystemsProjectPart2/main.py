"""
Author: Kyle Kolodziej
Created: July 12th, 2021
Last Updated: July 25th, 2021
"""
import operator
import sys
import numpy as np
from tabulate import tabulate

# Implement Shortest Job First (SJF) scheduling and Nonpreemptive Priority scheduling (Use only 1,2,3,4 for priorities and assume 1 is
# the highest priority). Compare these scheduling algorithms in terms of average
# waiting time on a given sample of processes.


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
    returnArray = []
    currTime = 0
    totalWaitTime = 0

    #first process here
    firstProcess = processArray[0]
    processArray.remove(firstProcess)
    firstProcess.setWaitTime(0)
    firstProcess.setTurnaroundTime(firstProcess.burstTime)
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
        newProcess.setWaitTime(currTime - newProcess.arrivalTime)
        currTime += newProcess.burstTime
        newProcess.setTurnaroundTime(currTime - newProcess.arrivalTime)
        returnArray.append(newProcess)
        del processArray[index]

    newProcess = processArray[0]
    newProcess.setWaitTime(currTime - newProcess.arrivalTime)
    currTime += newProcess.burstTime
    newProcess.setTurnaroundTime(currTime - newProcess.arrivalTime)
    returnArray.append(newProcess)



    return returnArray


def executeInputFile(inputFileName, algorithm):
    processArray = []
    print("\n----------------------------------------------------------------------------------------------")
    print("Input file being executed: " + inputFileName)
    if algorithm == "sjf":
        # Shortest Job First Algo
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
        # print("----------------------------------------------------------------------------------------------------------------------")
        # print("Process ID\t\t|\t\tArrival Time\t\t|\t\tBurst Time\t\t|\t\tWait Time\t\t|\t\tTurnaround Time")
        # print(
        #     "----------------------------------------------------------------------------------------------------------------------")


        orderedArray = runShortestJobFirst(processArray)
        columns = ('Process ID', 'Arrival Time', 'Burst Time', 'Priority', 'Wait Time', 'Turnaround Time')
        #columns = ('Process ID', 'Arrival Time', 'Burst Time', 'Priority')
        n_rows = len(orderedArray)
        cell_text = []
        for row in range(n_rows):
            processInfo = [orderedArray[row].processID, orderedArray[row].arrivalTime, orderedArray[row].burstTime, orderedArray[row].priority, orderedArray[row].waitTime, orderedArray[row].turnaroundTime]
            cell_text.append(processInfo)
        print(tabulate(cell_text, headers=columns, tablefmt="grid"))




        # for i in range(len(processArray)):
        #     print(processArray[i].processID + "\t\t\t\t|\t\t\t" + processArray[i].arrivalTime + "\t\t\t\t|\t\t\t" +
        #           processArray[i].burstTime + "\t\t\t|\t\t\t" + str(-1) + "\t\t\t|\t\t\t" + str(-2))
        #     print("----------------------------------------------------------------------------------------------------------------------")

    else:
        #Non preemptive
        print("Algorithm: Non-Preemptive Priority Scheduling")
        print("----------------------------------------------------------------------------------------------\n")
    return 0

print("----------------------------------------------------------------------------------------------------------------------\n")
print("Welcome to Kyle Kolodziej's Operating System's Project #2: Shortest Job First and Non-Preemptive Priority Scheduling!\n")
print("----------------------------------------------------------------------------------------------------------------------")

userInput = 0
while userInput != 3:
    print("-----------------------------------------------------------------------------------------------------")
    print("Would you like to...")
    print("\t1) Read through an Input file using Shortest Job First Scheduling")
    print("\t2) Read through an Input file using Non-Preemptive Priority Scheduling")
    print("\t3) Exit")
    print("-----------------------------------------------------------------------------------------------------\n")
    try:
        userInput = int(input("Please input your option (1-3): "))
        if 1 <= userInput <= 3:
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
                                userInput = 3
                                print("Exiting the program...")
                                print(
                                    "\n-----------------------------------------------------------------------------------------------------\n")
                                print("Thank you for using Kyle Kolodziej's Operating Systems Project Part 2! Goodbye!")
                                print(
                                    "\n-----------------------------------------------------------------------------------------------------\n")
                                break

                            # inputFileToAdd = True
                            # while inputFileToAdd:
                            #     try:
                            #
                            #         inputFile = input("Please enter the input file's name: ")
                            #         while inputFile == "":
                            #             inputFile = input("Error, no file name received! Please enter the input file's name: ")
                            #         if ".txt" not in inputFile:
                            #             # If user doesn't add the file type, make it a text file
                            #             inputFile = inputFile + ".txt"
                            #         fileOpened = open(inputFile, "r")
                            #         for line in fileOpened:
                            #             #process input file
                            #             if line.startswith("process"):
                            #                 pass
                            #             else:
                            #                 splittedString = line.split(',')
                            #                 processID = splittedString[0]
                            #                 priority = splittedString[1][1:]
                            #                 pcb.addProcess(processID, int(priority))
                            #         print("\nSuccessfully added Processes from: ", inputFile)
                            #         inputFileToAdd = False
                            #     except:
                            #         print("\nError! Unable to open the input file given! Please try again...")
                        else:
                            raise Exception
                    except:
                        print("\nError, invalid option! Please input a valid option!")

            elif userInput == 2:
                # Non-Preemptive Priority Algo
                processID = input("Please enter the Process ID: ")
                while processID == "":
                    processID = input("Error! No Process ID entered. Please enter a Process ID: ")
                print("Would you like to enter a priority for this process?")
                print("\t1) Yes")
                print("\t2) No")
                priorityChoice = 0
                while priorityChoice != 1 and priorityChoice != 2:
                    try:
                        priorityChoice = int(input("Please enter your choice (1 or 2): "))
                        if priorityChoice == 1 or priorityChoice == 2:
                            if priorityChoice == 1:
                                #User wants to enter the Process' priority value
                                needToAddProcess = True
                                while needToAddProcess:
                                    try:
                                        priority = int(input("\nPlease enter the priority (integer >= 1): "))
                                        if priority >= 1:
                                            pcb.addProcess(processID, priority)
                                            needToAddProcess = False
                                        else:
                                            raise Exception
                                    except:
                                        print("Error! Please enter a valid priority value!")
                            else:
                                #Priority is null, just add
                                pcb.addProcess(processID)
                            break
                        else:
                            raise Exception
                    except:
                        print("\nError, invalid option! Please input a valid option!")
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
