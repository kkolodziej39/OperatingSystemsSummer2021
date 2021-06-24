"""
Author: Kyle Kolodziej
Created: June 6th, 2021
Last Updated: June 23rd, 2021
"""
import sys
import numpy as np

class Process:
    """
    A class that will be used to represent a Process

    ...

    Attributes
    ----------
    processID : str
        a string that contains the Process ID of the Process (can be a mix of letters, numbers, and symbols)
    priority : int
        the priority value of the Process (1 being the highest priority...bigger numbers lower priority)
    next: Process
        each Process will have a pointer to the next Process in the Process Control Block
    """
    def __init__(self, processID, priority=None):
        """
        Parameters
        ----------
        :param processID: string
            a string that contains the Process ID of the Process (can be a mix of letters, numbers, and symbols)
        :param priority: int, optional
            the priority value of the Process (1 being the highest priority...bigger numbers lower priority)
            the default values is -1 (it doesn't have a priority)
        """
        self.processID = processID
        if priority is None:
            self.priority = -1
        else:
            self.priority = priority
        self.next = None

class ProcessControlBlock:
    """
        A class that will be used to represent a Process Control Block queue

        ...

        Attributes
        ----------
        head : Process
            the Process node containing the highest priority in the list of Processes
        tail : Process
            the Process node containing the lowest priority in the list of Processes

        Methods
        ----------
        printProcessControlBlock()
            print all of the Processes that the Process Control Block queue contains
        addProcess(processID, priority=None)
            used to add a Process to the Process Control Block
        """
    def __init__(self, processID=None, priority=None):
        """
        Construct the Process Control Board queue with or without a Process object

        :param processID: string, optional
            a string that contains the Process ID of the Process (can be a mix of letters, numbers, and symbols)
        :param priority: int, optional
            the priority value of the Process (1 being the highest priority...bigger numbers lower priority)
            the default values is -1 (it doesn't have a priority)
        """
        if processID is None: #Empty Process Control Board queue
            self.head = None
            self.tail = None
        else:
            process = Process(processID, priority)
            self.head = process
            self.tail = process

    def printProcessControlBlock(self):
        """
        Prints all of the Processes that the Process Control Block queue contains.
        For each Process, this function will print the Process':
            1) position in the Process Control Board queue
            2) process ID
            3) priority, or none if a priority does not exist

        Will print a message stating the Process Control Board queue is empty if no Processes exist
        :return: Nothing
        """
        print("Printing the Process Control Board queue...\n")
        if self.head is None:
            # Check if it is an empty Process Control Board queue, if so then tell the user the board is empty
            print("Process Control Board queue is empty!\n")
            return

        count = 1
        curr = self.head
        while curr is not None:
            if curr.priority != -1:
                print("[Position: {}, Process ID = {}, Priority = {}] ".format(count, curr.processID, curr.priority),
                      end="")
            else:
                print("[Position: {}, Process ID = {}, Priority = None] ".format(count, curr.processID),
                      end="")
            curr = curr.next
            count += 1
            if curr is not None:
                print("-----> ", end="")
        print("\n\n")
        return

    def addProcess(self, processID, priority=None):
        """
        Used to add a Process to the Process Control Block queue
        The default position (if no priority is given) is the end (tail) of the Process Control Board queue

        If multiple Processes have the same priority, the ordering for that priority will function like a
        FIFO queue (i.e. the Processes that were in the Process Control Board queue before will be farther up front)

        :param processID: string
            a string that contains the Process ID of the Process (can be a mix of letters, numbers, and symbols)
        :param priority: int, optional
            the priority value of the Process (1 being the highest priority...bigger numbers lower priority)
            the default values is -1 (it doesn't have a priority)
        :return: Nothing
        """

        process = Process(processID, priority)
        if self.head is None:
            self.head = process
            self.tail = process
        elif priority is None:
            # Add process to default position (the end/tail)
            prev = self.head
            curr = self.head.next
            while curr is not None:
                curr = curr.next
                prev = prev.next
            prev.next = process
            self.tail = process
        else:
            # Find where the Process should go in terms of priority
            if self.head.priority == -1:
                # Put Process at top of the Process Control Block queue as it has the highest priority
                # since the other Processes do not have a priority
                process.next = self.head
                self.head = process
            elif process.priority < self.head.priority:
                # Put Process at top of the Process Control Block queue as it has the highest priority
                process.next = self.head
                self.head = process
            else:
                # Not the highest priority, so need to iterate through the Process Control Board queue
                # to see where it goes
                prev = self.head
                curr = self.head.next
                while curr is not None and process.priority >= curr.priority and curr.priority != -1:
                    curr = curr.next
                    prev = prev.next
                prev.next = process
                process.next = curr
                if curr is None:
                    # Process is at the end of the Process Control Block queue
                    self.tail = process

    def deleteProcess(self, processID=None):
        """
        Used to delete a Process from the Process Control Board queue based on the process ID

        Default Process to delete is the start (head) of the Process Control Board queue
        Will tell the user if the Process Control Board queue is empty

        If the process ID does not exist within the Process Control Board queue, will print a message informing the user

        If the process ID passed in matches with one in the Process Control Board queue
        will print the following of the Process that is being deleted:
            1) position in the Process Control
            2) process ID
            3) priority, or none if a priority does not exist
        :param processID: str
            a string that contains the Process ID of the Process (can be a mix of letters, numbers, and symbols)
        :return: Nothing
        """
        print("Deleting Process with process ID '" + str(processID) + "'...\n")
        if self.head is None:
            # First start off by checking if the Process Control Board queue is empty
            print("Error! Not able to delete a Process...the Process Control Board queue is empty!\n\n")
            return
        elif processID is None:
            # Delete the head with no ID passed in
            # Start by moving the head up to the next node
            self.head = self.head.next
        else:
            # Search for the Process within the Process Control Board queue by its process ID
            if processID == self.head.processID:
                # Delete the head and print its contents
                print("Process Deleted: [Position: 1, Process ID: {}, Priority: {}]\n\n".format(processID,
                                                                                            self.head.priority))
                self.head = self.head.next
                # Now check if the head was the only process in the Process Control Board queue
                # and got deleted as will need to update the tail of the Process Control Board queue
                if self.head is None:
                    self.tail = None
            else:
                count = 2
                curr = self.head.next
                prev = self.head
                while curr.processID != processID and curr.next is not None:
                    curr = curr.next
                    prev = prev.next
                    count += 1

                if curr.processID != processID:
                    # The process ID passed in does not match any in the Process Control Board queue
                    print("Error! Process ID '{}' does not exist in the Process Control Board queue!\n\n".format(processID))
                else:
                    # Delete the Process and print its contents
                    print("Process Deleted: [Position: {}, Process ID: {}, Priority: {}]\n\n".format(count, processID,
                                                                                                 curr.priority))
                    prev.next = curr.next
                    # Now will check if deleted the tail from the Process Control Board queue
                    # as that will need to be updated
                    if curr.next is None:
                        self.tail = prev




print("-----------------------------------------------------------------------------------------------------\n")
print("Welcome to Kyle Kolodziej's Operating System's Project #1: Process Control Board queue Manipulation!\n")
print("-----------------------------------------------------------------------------------------------------\n")

userInput = 0
print("Would you like to...")
print("\t1) Add Process(es) via an Input File")
print("\t2) Add Process(es) via a process ID and priority from your input")
print("\t3) Delete a Process")
print("\t4) Exit\n")
while userInput != 4:
    try:
        userInput = int(input("Please input your option (1-4): "))
        if 1 <= userInput <= 4:
            if userInput == 1:
                print("add via file")
                break
            elif userInput == 2:
                print("add via input")
            elif userInput == 3:
                print("delete")
            else:
                print("Bye")
                break
            break
        raise Exception()
    except:
        print("\nError, invalid option! Please input a valid option!")


    # if userInput == 4:
    #     print("Bye")
    #     break
    #
    # while userInput < 1 or userInput > 4:
    #     userInput = int(input("\nError! Invalid option! Please input a valid option (1-4): "))




# pcb = ProcessControlBlock('1',2)
# #pcb.printProcessControlBlock()
# pcb.addProcess('12')
# #pcb.printProcessControlBlock()
# pcb.addProcess('11')
# #pcb.printProcessControlBlock()
# pcb.addProcess('12', 2)
#
# pcb.printProcessControlBlock()
# # for i in range(20):
# #     pcb.addProcess(np.random.randint(1, 1000000), i)
# pcb.deleteProcess('12')
# pcb.printProcessControlBlock()
