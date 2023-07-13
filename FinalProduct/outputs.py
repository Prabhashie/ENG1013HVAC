"""
Project:        ENG1013 HVAC
File:           outputs.py
Purpose:        This file controls an LED array based on the temperature readings along with console outputs
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
import shared
import math
import time

# global vars

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
    # pin mode set during system initialization
    if shared.ambientTempLow <= currTemp <= shared.ambientTempHigh: # if current temperature is within goal temp range
        shared.mode = 0 # no fans are on, mode is neither heating nor cooling
        # clear output pins
        # fans should be off - this is done because we cannot run different functionality asynchronously (only synchronous calls are in the unit scope)
        shared.board.digital_write(shared.blueLEDPin, 0)
        shared.board.digital_write(shared.redLEDPin, 0)
        shared.board.digital_write(shared.highLEDPin, 0)
        shared.board.digital_write(shared.lowLEDPin, 0)
        message = f"Current temperature {currTemp} is within the goal range {shared.ambientTempLow} - {shared.ambientTempHigh} C."
        print_to_console(message)
    else:
        # pin mode set during system initialization
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
    # pin mode set during system initialization
    # CHECK: might need to use a loop to run the fan (light LEDs) for some time
    if (currTemp < shared.ambientTempLow) and (shared.outsideTemperature >= shared.ambientTempLow): # if current temperature is lower than and outside temperature is greater than lower threshold
        shared.mode = 1 # heating mode on
        shared.systemModeMap.append((time.time(), shared.mode))

        # a RED LED turns on to indicate that the fan should move heat into the room
        shared.board.digital_write(shared.blueLEDPin, 0)
        shared.board.digital_write(shared.redLEDPin, 1)
        # time.sleep(2) # pause the execution of your Arduino program for 2s
        
        # 2 LEDs should be used, to indicate a low and high ventilation speed
        if (trend <= 0):
            shared.board.digital_write(shared.lowLEDPin, 0)
            shared.board.digital_write(shared.highLEDPin, 1)
            # time.sleep(2)
        else:
            shared.board.digital_write(shared.highLEDPin, 0)
            shared.board.digital_write(shared.lowLEDPin, 1)
            # time.sleep(2)
        
        # a console alert is printed.
        message = f"Current temperature {currTemp} is less than the lower goal threshold {shared.ambientTempLow} C."
        print_to_console(message)
    elif (currTemp > shared.ambientTempHigh) and (shared.outsideTemperature <= shared.ambientTempHigh): # if current temperature is higher than and outside temperature is lower than higher threshold
        shared.mode = -1 # cooling mode on
        shared.systemModeMap.append((time.time(), shared.mode))

        # a BLUE LED turns on to indicate that the fan should move heat out of the room
        shared.board.digital_write(shared.redLEDPin, 0)
        shared.board.digital_write(shared.blueLEDPin, 1) 
        # time.sleep(2)
        
        # 2 LEDs should be used, to indicate a low and high ventilation speed
        if (trend <= 0):
            shared.board.digital_write(shared.highLEDPin, 0)
            shared.board.digital_write(shared.lowLEDPin, 1)
            # time.sleep(2)
        else:
            shared.board.digital_write(shared.lowLEDPin, 0)
            shared.board.digital_write(shared.highLEDPin, 1)
            # time.sleep(2)
        
        # a console alert is printed.
        message = f"Current temperature {currTemp} is higher than the upper goal threshold {shared.ambientTempHigh} C."
        print_to_console(message)
    else:
        shared.mode = 0 # no fans are on, mode is neither heating nor cooling
        # a console alert is printed.
        message = f"Current temperature is not within the ambient range but outside the room has extreme conditions!"
        print_to_console(message)
    
    # clear output pins
    # fans should be off - this is done because we cannot run different functionality asynchronously (only synchronous calls are in the unit scope)
    # shared.board.digital_write(shared.blueLEDPin, 0)
    # shared.board.digital_write(shared.redLEDPin, 0)
    # shared.board.digital_write(shared.highLEDPin, 0)
    # shared.board.digital_write(shared.lowLEDPin, 0)

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
    # pin mode set during system initialization
    scrollingStartTime = time.time()
    string = string.upper()
    stringLength = len(string)
    while time.time() - scrollingStartTime < scrollDuration:
        for i in range(stringLength - 3):
            substring = string[i : i + 4]
            display_four_character_string(substring, displayDuration)
    """
    for _ in range(8): # turn off all digits - can use CLR pin in the shift reg at the cost of an additional arduino pin
        shared.board.digital_write(pinSER1, 0)
        shared.board.digital_write(pinSRCLK1, 1)
        shared.board.digital_write(pinSRCLK1, 0)
        
    shared.board.digital_write(pinRCLK1, 1)
    shared.board.digital_write(pinRCLK1, 0)
    for i in digitPins: # turn off all digit pins (set to one as digit pins are active low)
        shared.board.digital_write(i,1)
    """

"""
Function to display a 4-digit alphanumeric message
Params: string    -> string to print
        duration  -> duration to disp the message
Return: None
"""
def display_four_character_string(string, duration):
    # pin mode set during system initialization
    string = string.upper() # turn the string to all upper case
    fourCharacterStartTime = time.time()
    while time.time() - fourCharacterStartTime < duration:
        for i in range(4):
            display_character(string[i], i+1)

    # clear output pins
    for _ in range(8): # turn off all digits - can use CLR pin in the shift reg at the cost of an additional arduino pin
        shared.board.digital_write(shared.pinSER1, 0)
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)

    shared.board.digital_write(shared.pinRCLK1, 1)
    shared.board.digital_write(shared.pinRCLK1, 0)
    for i in shared.digitPins: # turn off all digit pins (set to one as digit pins are active low)
        shared.board.digital_write(i,1)

"""
Function to display a character in the 7 seg
Params: character   -> char to display
        digit       -> digit to turn on
Return: None
"""
def display_character(character, digit):
    # pin mode set during system initialization
    segments = shared.CHAR_MAP[character]
    for i in shared.digitPins:
        shared.board.digital_write(i, 1) # turn off all digits
    for _ in range(8): # clear all the segments and turn off
        shared.board.digital_write(shared.pinSER1, 0)
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)

    shared.board.digital_write(shared.pinRCLK1, 1)
    shared.board.digital_write(shared.pinRCLK1, 0)
    
    # pins should be written g - a
    # connect the shift reg to the 7 seg accordingly
    for i in range(6, -1, -1): # write value to the 7 seg
        shared.board.digital_write(shared.pinSER1, segments[i])
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)
   
    shared.board.digital_write(shared.pinRCLK1, 1)
    shared.board.digital_write(shared.pinRCLK1, 0)
    
    shared.board.digital_write(shared.digitPins[digit - 1], 0) # turn on the digit pin
    time.sleep(0.025)

"""
Function to display temperatures on thermometer
Params: temp -> temperature to display
Return: None
< 18
18 - 20
20 - 22
22 - 24
24 - 26
26 - 28
28 - 30
> 30
"""
def display_temeprature(temp):
    # pin mode set during system initialization
    if temp < 18:
        code = shared.TEMP_MAP[0]
    elif 18 <= temp < 20:
        code = shared.TEMP_MAP[1]
    elif 20 <= temp < 22:
        code = shared.TEMP_MAP[2]
    elif 22 <= temp < 24:
        code = shared.TEMP_MAP[3]
    elif 24 <= temp < 26:
        code = shared.TEMP_MAP[4]
    elif 26 <= temp < 28:
        code = shared.TEMP_MAP[5]
    elif 28 <= temp < 30:
        code = shared.TEMP_MAP[6]
    else:
        code = shared.TEMP_MAP[7]

    for _ in range(8): # clear all the segments and turn off
        shared.board.digital_write(shared.pinSER2, 0)
        shared.board.digital_write(shared.pinSRCLK2, 1)
        shared.board.digital_write(shared.pinSRCLK2, 0)

    shared.board.digital_write(shared.pinRCLK2, 1)
    shared.board.digital_write(shared.pinRCLK2, 0)

    for i in range(8):
        shared.board.digital_write(shared.pinSER2, code[i])
        shared.board.digital_write(shared.pinSRCLK2, 1)
        shared.board.digital_write(shared.pinSRCLK2, 0)
   
    shared.board.digital_write(shared.pinRCLK2, 1)
    shared.board.digital_write(shared.pinRCLK2, 0)
    
"""
Function to flash LED and sound buzzer based on change of temperature
Params: trend -> if the temperature is increasing or decreasing or stable in the current temperature range
Return: None
"""
def alert_change(trend):
    # pin mode set during system initialization
    if trend != 0: # if temperature is changing
        # flash LED
        shared.board.digital_write(shared.flashingLEDPin, 1)
        if trend == 1: # increasing temperature
            shared.board.digital_write(shared.buzzerPin2, 0)
            shared.board.digital_write(shared.buzzerPin1, 1)
            display_four_character_string("RISE", 0.5)
        else: # decreasing temperature
            shared.board.digital_write(shared.buzzerPin1, 0)
            shared.board.digital_write(shared.buzzerPin2, 1)
            display_four_character_string("FALL", 0.5)
    else:
        shared.board.digital_write(shared.buzzerPin1, 0)
        shared.board.digital_write(shared.buzzerPin2, 0)

    # time.sleep(0.5)
    # clear output pins
    # shared.board.digital_write(shared.flashingLEDPin, 0)
    # shared.board.digital_write(shared.buzzerPin1, 0)
    # shared.board.digital_write(shared.buzzerPin2, 0)

"""
Function to show response to ultrasonic sensor (door opened)
Params: None
Return: None
"""
def ultrasonicResponse():
    # pin mode set during system initialization
    shared.board.digital_write(shared.ultrasonicResponsePin, shared.isDoorOpen)

"""
Function to show response to LDR sensor (lighting changed)
Params: None
Return: None
"""
def ldrResponse():
    # pin mode set during system initialization
    shared.board.digital_write(shared.ldrResponsePin, shared.isLightingNotAmbient)

"""
Function to force switch fan modes (LEDs)
Params: None
Return: None
"""
def force_control_leds():
    # pin mode set during system initialization
    if shared.mode == 1: # switch to heating
        print("Setting red")
        shared.board.digital_write(shared.blueLEDPin, 0)
        shared.board.digital_write(shared.redLEDPin, 1)
    elif shared.mode == -1:
        print("Setting blue")
        shared.board.digital_write(shared.redLEDPin, 0)
        shared.board.digital_write(shared.blueLEDPin, 1) 
    
    # time.sleep(0.5)
    # clear output pins
    # shared.board.digital_write(shared.redLEDPin, 0)
    # shared.board.digital_write(shared.blueLEDPin, 0)
