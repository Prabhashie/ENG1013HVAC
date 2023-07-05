"""
Project:        ENG1013 HVAC
File:           outputs.py
Purpose:        This file controls an LED array based on the temperature readings along with console outputs
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from shared import *
import math
import time

# global vars
redLEDPin = 1
blueLEDPin = 2
lowLEDPin = 3
highLEDPin = 4

"""
Function to control LED array and console output based on temperature reading
Params: currTemp    -> current temperature of the room
        trend       -> if the temperature is increasing or decreasing or stable in the current temperature range
Return: None
1. if the current temperature is in the hot region, fan should move heat out
2. if the current temperature is greater than the previous temperature, fan should move heat out fast => increase fan spead
3. if the current temperature is smaller than the previous temperature, fan should move heat out slow => decrease fan spead
"""
def displayTemp(currTemp, trend):
    if ambientTempLow <= currTemp <= ambientTempHigh: # if current temperature is within goal temp range
        message = f"Current temperature {currTemp} is within the goal range {ambientTempLow} - {ambientTempHigh} C."
        printToConsole(message)
    else:
        pinList = [redLEDPin, blueLEDPin, lowLEDPin, highLEDPin]
        setDigitalOutputPinMode(pinList)
        controlLEDs(currTemp, trend)
        
"""
Function to control LED array
Params: currTemp    -> current temperature of the room
        trend       -> if the temperature is increasing or decreasing or stable in the current temperature range
Return: None
"""
def controlLEDs(currTemp, trend):
    # CHECK: might need to use a loop to run the fan (light LEDs) for some time
    if currTemp < ambientTempLow: # if current temperature is lower than goal threshold
        # a RED LED turns on to indicate that the fan should move heat into the room
        board.digital_write(blueLEDPin, 0)
        board.digital_write(redLEDPin, 1) # CHECK: would this be left lit forever if not set to 0?
        time.sleep(2) # pause the execution of your Arduino program for 2s
        # CHECK: need to set to low after sleep?
        # 2 LEDs should be used, to indicate a low and high ventilation speed
        if (trend <= 0):
            board.digital_write(highLEDPin, 0)
            board.digital_write(lowLEDPin, 1)
            time.sleep(2)
        else:
            board.digital_write(lowLEDPin, 0)
            board.digital_write(highLEDPin, 1)
            time.sleep(2)
        # a console alert is printed.
        message = f"Current temperature {currTemp} is less than the lower goal threshold {ambientTempLow} C."
        printToConsole(message)
    else: # if current temperature is higher than goal threshold
        # a BLUE LED turns on to indicate that the fan should move heat out of the room
        board.digital_write(redLEDPin, 0)
        board.digital_write(blueLEDPin, 1) 
        time.sleep(2)
        # 2 LEDs should be used, to indicate a low and high ventilation speed
        if (trend <= 0):
            board.digital_write(highLEDPin, 0)
            board.digital_write(lowLEDPin, 1)
            time.sleep(2)
        else:
            board.digital_write(lowLEDPin, 0)
            board.digital_write(highLEDPin, 1)
            time.sleep(2)
        # a console alert is printed.
        message = f"Current temperature {currTemp} is higher than the upper goal threshold {ambientTempHigh} C."
        printToConsole(message)

"""
Function to print outputs to console
Params: message     -> Message to pprint
Return: None
"""
def printToConsole(message):
    print(message)

def control7Seg():
    pass