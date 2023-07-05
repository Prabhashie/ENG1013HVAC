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

# global vars

"""
Function to graph temperature variation over the last 20s
Params: None
Return: None
"""
def graphing():
    timeData = []
    temperatureData = []
    for item in temperatureMap:
        timeData.append(item[0])
        temperatureData.append(item[1])
    print("Graphing variation of temperature over past 20s...")
    pyplot.plot(timeData, temperatureData, "*")
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Temperature (C)')
    pyplot.title("Temperature variation inside the room within the last 20s")
    pyplot.show()