"""
Project:        ENG1013 HVAC
File:           graphing.py
Purpose:        This file handles the graph operations of the system
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from shared import *
from matplotlib import pyplot
import sys
from datetime import datetime

# global vars

"""
Function to produce graphs
Params: None
Return: None
"""
def graphing():
    # loop if an incorrect input is entered
    while True:
        print("Please select from the below options: \n1. Time Vs. Temp \n2. TODO \n3. TODO \n") 
        try:
            userInput = int(input("Your Choice: "))
            if (userInput not in [1,2,3]):
                print("Invalid selection! Please choose again.\n")
                continue
        except ValueError:
            print("Please enter a value between 1 and 3.\n")
        except KeyboardInterrupt:
            print("\nExiting system...\n")
            return

        # call relavent function
        if userInput == 1:
            graphTimeVsTemp()
        elif userInput == 2:
            pass
        elif userInput == 3:
            pass
    

def graphTimeVsTemp():
    timeData = []
    temperatureData = []
    for item in temperatureMap:
        timeData.append(item[0] - temperatureMap[0][0]) # display the time axis between 0-20s
        temperatureData.append(item[1])
    print("Graphing variation of temperature over past 20s...")
    pyplot.plot(timeData, temperatureData, "*")
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Temperature (C)')
    pyplot.xlim([0, 20])
    pyplot.title("Temperature variation inside the room within the last 20s")
    pyplot.savefig(f'results/TimeVsTemp_{datetime.now().strftime("%Y%m%d%H%M%S")}.png') # https://mljar.com/blog/matplotlib-save-plot/
    pyplot.show()

# TODO: add remaining graphing choices