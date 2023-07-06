"""
Project:        ENG1013 HVAC
File:           controlSystem.py
Purpose:        This file contains the invocation of the polling loop/ fan operation of the HVAC
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from inputs import readThermistor
from outputs import displayTemp
from shared import *
import time
import sys

# global vars

"""
Function to run the polling loop for fan operation
Params: None
Return: None
"""
def controlSystem():
    try:
        while True:
            startLoop = time.time()
            currTemp, currTime = readThermistor()
            prevTemp = currTemp if len(temperatureMap) == 0 else temperatureMap[-1][1] # get last recorded temperature. if array is empty, use current value

            while (len(temperatureMap) != 0) and ((currTime - temperatureMap[0][0]) > 20): # only keep the temperature data from last 20s
                temperatureMap.pop(0)
            temperatureMap.append((currTime, currTemp))
            trend = 1 if currTemp - prevTemp > 0 else -1 if currTemp - prevTemp < 0 else 0 # check if the temperature is increasing/ decreasing or constant
            # if the current temperature is in the hot region, fan should move heat out
            # if the current temperature is greater than the previous temperature, fan should move heat out fast => increase fan spead
            # if the current temperature is smaller than the previous temperature, fan should move heat out slow => decrease fan spead
            displayTemp(currTemp, trend)
            endLoop = time.time()
            print(f"Time taken by the polling loop: {endLoop - startLoop}")
    except KeyboardInterrupt:
        print("\nExiting control system...")
        board.shutdown()
        sys.exit(0)

controlSystem()