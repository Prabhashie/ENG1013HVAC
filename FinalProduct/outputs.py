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
Function to display a 4-digit alphanumeric message -with scrolling
Params: string          -> string to print
        scrollDuration  -> duration to scroll
        displayDuration -> duration of display in seconds
Return: None
"""
def display_scrolling_string(string, scrollDuration, displayDuration):
    scrollingStartTime = time.time()
    stringLength = len(string)
    while time.time()-scrollingStartTime<displayDuration:
        for i in range(stringLength - 3):
            substring = string[i : i + 4]
            display_four_character_string(substring, scrollDuration)
    for i in [1,2,3,4,5,6,7,8]:
        board.digital_write(pinSRCLK,0)
        board.digital_write(pinSER,0)
        board.digital_write(pinSRCLK,1)
    board.digital_pin_write(pinRCLK,1)
    board.digital_pin_write(pinRCLK,0)
    for i in digitPins:
        board.digital_write(i,1)

def display_four_character_string(string,duration):
    fourCharacterStartTime = time.time()
    while time.time()-fourCharacterStartTime<duration:
        for i in range(4):
            display_character(string[i],i+1)
    for i in [1,2,3,4,5,6,7,8]:
        board.digital_write(pinSRCLK,0)
        board.digital_write(pinSER,0)
        board.digital_write(pinSRCLK,1)
    board.digital_pin_write(pinRCLK,1)
    board.digital_pin_write(pinRCLK,0)
    for i in digitPins:
        board.digital_write(i,1)

def display_character(character,digit):
    # digit 1 is pin 16
    # digit 2 is pin 17
    # digit 3 is pin 18
    # digit 4 is pin 19
    # segment a is pin h on shift register
    # segment b is pin b on shift register
    # segment c is pin c on shift register
    # segment d is pin d on shift register
    # segment e is pin e on shift register
    # segment f is pin f on shift register
    # segment g is pin g on shift register
    # Thermistor buzzer is pin a on shift register
    # TODO clear the shift register here
    segments = charMap[character]
    for i in digitPins:
        board.digital_write(i,1)
    for i in [1,2,3,4,5,6,7,8]:
        board.digital_write(pinSRCLK,0)
        board.digital_write(pinSER,0)
        board.digital_write(pinSRCLK,1)
    board.digital_pin_write(pinRCLK,1)
    board.digital_pin_write(pinRCLK,0)
    for i in [0,6,5,4,3,2,1]:
        if segments[i] == 1:
            board.digital_write(pinSRCLK,0)
            board.digital_write(pinSER,1)
            board.digital_write(pinSRCLK,1)
        elif segments[i] == 0:
            board.digital_write(pinSRCLK,0)
            board.digital_write(pinSER,0)
            board.digital_write(pinSRCLK,1)
    board.digital_write(pinSRCLK,0)
    if buzzer == True:
        board.digital_write(pinSER,1)
    else:
        board.digital_write(pinSER,0)
    board.digital_write(pinSRCLK,1)   
    board.digital_pin_write(pinRCLK,1)
    board.digital_pin_write(pinRCLK,0)
    if digit == 1:
        board.digital_pin_write(16,0)
    if digit == 2:
        board.digital_pin_write(17,0)
    if digit == 3:
        board.digital_pin_write(18,0)
    if digit == 4:
        board.digital_pin_write(19,0)
    time.sleep(0.025)
