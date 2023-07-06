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
eightSegPins = [i for i in range(1,9)]
digitPins = [9, 10, 11, 12]

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
        board.digital_write(redLEDPin, 1)
        # time.sleep(2) # pause the execution of your Arduino program for 2s
        # 2 LEDs should be used, to indicate a low and high ventilation speed
        if (trend <= 0):
            board.digital_write(highLEDPin, 0)
            board.digital_write(lowLEDPin, 1)
            # time.sleep(2)
        else:
            board.digital_write(lowLEDPin, 0)
            board.digital_write(highLEDPin, 1)
            # time.sleep(2)
        # a console alert is printed.
        message = f"Current temperature {currTemp} is less than the lower goal threshold {ambientTempLow} C."
        printToConsole(message)
    else: # if current temperature is higher than goal threshold
        # a BLUE LED turns on to indicate that the fan should move heat out of the room
        board.digital_write(redLEDPin, 0)
        board.digital_write(blueLEDPin, 1) 
        # time.sleep(2)
        # 2 LEDs should be used, to indicate a low and high ventilation speed
        if (trend <= 0):
            board.digital_write(highLEDPin, 0)
            board.digital_write(lowLEDPin, 1)
            # time.sleep(2)
        else:
            board.digital_write(lowLEDPin, 0)
            board.digital_write(highLEDPin, 1)
            # time.sleep(2)
        # a console alert is printed.
        message = f"Current temperature {currTemp} is higher than the upper goal threshold {ambientTempHigh} C."
        printToConsole(message)

"""
Function to print outputs to console
Params: message     -> Message to print
Return: None
"""
def printToConsole(message):
    print(message)

"""
Function to display a 4-digit alphanumeric message - without shift reg and no scrolling
Params: message     -> Message to print
        duration    -> duration of display in seconds
Return: None
"""
def control7Seg(message, duration):
    message = message[:4] # make sure the message has only 4 chars
    setDigitalOutputPinMode(eightSegPins)
    setDigitalOutputPinMode(digitPins)
    startTime = 0
    while startTime < duration:
        for i in range(len(message)): # 1st pin in digitPins is connected to left most digit in the 4-digit 8 seg
            binCode = alphabet[message[i].upper()] # takes chars in message from left to right
            board.digital_write(digitPins[i], 0)
            for j in range(8): # write from segment a - dp assuming 1st pin in eightSegPins is connected to seg 'a'
                if (binCode) & (PIN_MASK >> j):
                    board.digital_write(eightSegPins[j], 1)
                else:
                    board.digital_write(eightSegPins[j], 0)
            startTime += 0.25
            time.sleep(0.25) # each char is displayed for 0.25s
            board.digital_write(digitPins[i], 1)



            charMap = {
    '0': [1, 1, 1, 1, 1, 1, 0],
    '1': [0, 1, 1, 0, 0, 0, 0],
    '2': [1, 1, 0, 1, 1, 0, 1],
    '3': [1, 1, 1, 1, 0, 0, 1],
    '4': [0, 1, 1, 0, 0, 1, 1],
    '5': [1, 0, 1, 1, 0, 1, 1],
    '6': [1, 0, 1, 1, 1, 1, 1],
    '7': [1, 1, 1, 0, 0, 0, 0],
    '8': [1, 1, 1, 1, 1, 1, 1],
    '9': [1, 1, 1, 1, 0, 1, 1],
    'A': [1, 1, 1, 0, 1, 1, 1],
    'B': [0, 0, 1, 1, 1, 1, 1],
    'C': [1, 0, 0, 1, 1, 1, 0],
    'D': [0, 1, 1, 1, 1, 0, 1],
    'E': [1, 0, 0, 1, 1, 1, 1],
    'F': [1, 0, 0, 0, 1, 1, 1],
    'G': [1, 0, 1, 1, 1, 1, 0],
    'H': [0, 0, 1, 0, 1, 1, 1],
    'I': [0, 0, 0, 0, 1, 1, 0],
    'J': [0, 1, 1, 1, 1, 0, 0],
    'K': [1, 0, 1, 0, 1, 1, 1],
    'L': [0, 0, 0, 1, 1, 1, 0],
    'M': [1, 0, 1, 0, 1, 0, 0],
    'N': [1, 1, 1, 0, 1, 1, 0],
    'O': [1, 1, 1, 1, 1, 1, 0],
    'P': [1, 1, 0, 0, 1, 1, 1],
    'Q': [1, 1, 1, 0, 0, 1, 1],
    'R': [0, 0, 0, 1, 0, 1, 0],
    'S': [1, 0, 1, 1, 0, 1, 1],
    'T': [0, 0, 0, 1, 1, 1, 1],
    'U': [0, 1, 1, 1, 1, 1, 0],
    'V': [0, 1, 1, 1, 0, 1, 0],
    'W': [0, 1, 0, 1, 0, 1, 0],
    'X': [0, 1, 1, 0, 1, 1, 1],
    'Y': [0, 1, 1, 1, 0, 1, 1],
    'Z': [1, 1, 0, 1, 0, 0, 1],
    '_': [0, 0, 0, 0, 0, 0, 0]
}