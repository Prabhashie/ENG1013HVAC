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
    a. if the current temperature is greater than the previous temperature, fan should move heat out fast => increase fan spead
    b. if the current temperature is smaller than the previous temperature, fan should move heat out slow => decrease fan spead
2. vice versa when current temperature is in the cold region
"""
def control_room_environment(currTemp, trend):
    if ambientTempLow <= currTemp <= ambientTempHigh: # if current temperature is within goal temp range
        # fans should be off
        board.digital_write(blueLEDPin, 0)
        board.digital_write(redLEDPin, 0)
        board.digital_write(highLEDPin, 0)
        board.digital_write(lowLEDPin, 0)

        message = f"Current temperature {currTemp} is within the goal range {ambientTempLow} - {ambientTempHigh} C."
        print_to_console(message)
    else:
        pinList = [redLEDPin, blueLEDPin, lowLEDPin, highLEDPin]
        set_digital_output_pin_mode(pinList)
        control_leds(currTemp, trend)
        
"""
Function to control LED array
Params: currTemp    -> current temperature of the room
        trend       -> if the temperature is increasing or decreasing or stable in the current temperature range
Return: None
Usage of the 2nd thermistor
    we do not want to equate the temperature inside to temperature outside
    ambient temp inside the room is decided based on the user defined ambient thresholds
    2nd thermistor is used to check if we need to move air in from outside when the environment inside the room is not ambient
    ex: if inside the room is hot and outside is hotter, even if we want to move heat out, we shouldn't do this since air outside is hotter
    ex: if inside is cold and outside is colder, even if we want to move heat in, we shouldn't do this since air outside is colder 
"""
def control_leds(currTemp, trend):
    # CHECK: might need to use a loop to run the fan (light LEDs) for some time
    if (currTemp < ambientTempLow) and (outsideTemperature >= ambientTempLow): # if current temperature is lower than and outside temperature is greater than lower threshold
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
        print_to_console(message)
    elif (currTemp > ambientTempHigh) and (outsideTemperature <= ambientTempHigh): # if current temperature is higher than and outside temperature is lower than higher threshold
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
        print_to_console(message)
    else:
        # a console alert is printed.
        message = f"Current temperature is not within the ambient range but outside the room has extreme conditions!"
        print_to_console(message)

"""
Function to print outputs to console
Params: message     -> Message to print
Return: None
"""
def print_to_console(message):
    print(message)

"""
Function to display a 4-digit alphanumeric message with scrolling
Params: string          -> string to print
        scrollDuration  -> the amount of time the scrolled message will be displayed for 
        displayDuration -> the duration each 4 letter substring of the scrolled messsage will display
Return: None
scrollDuration > displayDuration
"""
def display_scrolling_string(string, scrollDuration, displayDuration):
    set_digital_output_pin_mode([pinSER, pinSRCLK, pinRCLK])
    set_digital_output_pin_mode(digitPins)

    scrollingStartTime = time.time()
    string = string.upper()
    stringLength = len(string)
    while time.time() - scrollingStartTime < scrollDuration:
        for i in range(stringLength - 3):
            substring = string[i : i + 4]
            display_four_character_string(substring, displayDuration)
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
        board.digital_write(i, 1) # turn off all digits
    for _ in range(8): # clear all the segments and turn off
        board.digital_write(pinSER, 0)
        board.digital_write(pinSRCLK, 1)
        board.digital_write(pinSRCLK, 0)

    board.digital_write(pinRCLK, 1)
    board.digital_write(pinRCLK, 0)
    
    # pins should be written g - a
    # connect the shift reg to the 7 seg accordingly
    for i in range(6, -1, -1): # write value to the 7 seg
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
def force_control_leds():
    if mode: # switch to heating
        board.digital_write(blueLEDPin, 0)
        board.digital_write(redLEDPin, 1)
    else:
        board.digital_write(redLEDPin, 0)
        board.digital_write(blueLEDPin, 1) 
