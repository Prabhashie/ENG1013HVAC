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
redLEDPin = 7
blueLEDPin = 8
lowLEDPin = 3
highLEDPin = 4
eightSegPins = [i for i in range(1,9)]
digitPins = [9, 10, 11, 12]
pinSRCLK = 1
pinSER = 2
pinRCLK = 3

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

"""
Function to display a 4-digit alphanumeric message with scrolling
Params: string          -> string to print
        scrollDuration  -> duration to scroll
        displayDuration -> duration of display in seconds
Return: None
"""
def display_scrolling_string(string, scrollDuration, displayDuration):
    setDigitalOutputPinMode([pinSER, pinSRCLK, pinRCLK])
    setDigitalOutputPinMode(digitPins)

    scrollingStartTime = time.time()
    stringLength = len(string)
    while time.time() - scrollingStartTime < displayDuration:
        for i in range(stringLength - 3):
            substring = string[i : i + 4]
            display_four_character_string(substring, scrollDuration)
    for _ in range(8): # turn off all digits
        board.digital_write(pinSER, 0)
        board.digital_write(pinSRCLK, 1)
        board.digital_write(pinSRCLK, 0)
        
    board.digital_write(pinRCLK, 1)
    board.digital_write(pinRCLK, 0)
    for i in digitPins: # turn off all digit pins (set to one as digit pins are active low)
        board.digital_write(i,1)

"""
Function to display a 4-digit alphanumeric message
Params: string    -> string to print
        duration  -> duration to disp the message
Return: None
"""
def display_four_character_string(string, duration):
    fourCharacterStartTime = time.time()
    while time.time() - fourCharacterStartTime < duration:
        for i in range(4):
            display_character(string[i], i+1)
    for _ in range(8): # turn off all digits
        board.digital_write(pinSER, 0)
        board.digital_write(pinSRCLK, 1)
        board.digital_write(pinSRCLK, 0)

    board.digital_write(pinRCLK, 1)
    board.digital_write(pinRCLK, 0)
    for i in digitPins: # turn off all digit pins (set to one as digit pins are active low)
        board.digital_write(i,1)

"""
Function to display a character in the 7 seg
Params: character   -> char to display
        digit       -> digit to turn on
Return: None
"""
def display_character(character, digit):

    segments = charMap[character]
    for i in digitPins:
        board.digital_write(i, 1)
    for _ in range(8): # turn off all digits
        board.digital_write(pinSER, 0)
        board.digital_write(pinSRCLK, 1)
        board.digital_write(pinSRCLK, 0)

    board.digital_write(pinRCLK, 1)
    board.digital_write(pinRCLK, 0)
    
    # pins should be written a - g
    # connect the shift reg to the 7 seg accordingly
    for i in range(7): # write value to the 7 seg
        board.digital_write(pinSER, segments[i])
        board.digital_write(pinSRCLK, 1)
        board.digital_write(pinSRCLK, 0)
   
    board.digital_write(pinRCLK, 1)
    board.digital_write(pinRCLK, 0)
    
    board.digital_write(digitPins[digit - 1], 0) # turn on the digit pin
    time.sleep(0.025)

# TODO: Thermometer 

# TODO: Flashing LED
    # one for both rapidly increasing and decreasing
    
# TODO: Buzzer
    # one tone for each rapidly increasing and decreasing

# TODO: Response to Ultrasonic

# TODO: Response to LDR

"""
Function to force switch fan modes (LEDs)
Params: None
Return: None
"""
def forceControlLEDs():
    if mode: # switch to heating
        board.digital_write(blueLEDPin, 0)
        board.digital_write(redLEDPin, 1)
    else:
        board.digital_write(redLEDPin, 0)
        board.digital_write(blueLEDPin, 1) 
