"""
Project:        ENG1013 HVAC
File:           main.py
Purpose:        This file runs the core functionality of the HVAC project. These include,
                1. Control System
                2. System Settings
                3. Graphing
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from controlSystem import control_system
from systemSettings import system_settings
from graphing import graphing
from outputs import display_scrolling_string
import shared
import time
import sys
import math

# global vars

"""
Function to display system menu
Params: None
Return: None
"""
def main():
    # get user input
    print("Welcome to ENG1013 Smart Fan System!\n")

    # init all arduino pins
    init_pins()

    # show scrolling welcome message message - one message is enough to demonstrate scrolling messages
    welcomeMessage = "Welcome to Smart HVAC"
    scrollDuration = 5
    displayDuration = 2
    display_scrolling_string(welcomeMessage, scrollDuration, displayDuration)

    # loop if an incorrect input is entered
    while True:
        print("Please select from the below options: \n1. Control System \n2. System Settings \n3. Graphing\n") 
        try:
            userInput = int(input("Your Choice: "))
            if (userInput not in [1,2,3]):
                print("Invalid selection! Please choose again.\n")
                continue
        except ValueError:
            print("Please enter a value between 1 and 3.\n")
        except KeyboardInterrupt:
            print("\nExiting system...\n")
            # clear all arduino pins
            clear_pins()
            shared.board.shutdown()
            sys.exit(0)
        except:
            # clear all arduino pins
            clear_pins()
            shared.board.shutdown()
            sys.exit(0)

        # call relavent function
        if userInput == 1:
            print("\nTaking you to control system...")
            control_system()
        elif userInput == 2:
            if (time.time() > shared.invalidPINTimeoutStart + 120):
                print("\nTaking you to system settings...")
                system_settings()
            else:
                print(f"\nSystem settings currently locked. Please try in {math.ceil(120-(time.time()-shared.invalidPINTimeoutStart))} seconds")
        elif userInput == 3:
            print("\nTaking you to graphing...")
            graphing()

"""
Function to init all arduino pins
Params: None
Return: None
"""
def init_pins():
    print("Initializing system...\n")
    # digital input pins
    shared.set_digital_input_pin_mode([shared.pushButtonPin])
    # analog input pins
    shared.set_analog_input_pin_mode([shared.thermistorPinIn, shared.thermistorPinOut, shared.ldrPin]) # callback function not set as temperature values are averaged over time
    # sonar pins
    shared.set_sonar_input_pin_mode([shared.triggerPin, shared.echoPin])
    # digital output pins
    pinList = [
        shared.redLEDPin, 
        shared.blueLEDPin, 
        shared.lowLEDPin, 
        shared.highLEDPin, 
        shared.flashingLEDPin, 
        shared.pinSER1, 
        shared.pinSRCLK1, 
        shared.pinRCLK1, 
        shared.pinSER2, 
        shared.pinSRCLK2, 
        shared.pinRCLK2, 
        shared.buzzerPin1, 
        shared.buzzerPin2
    ]
    shared.set_digital_output_pin_mode(pinList)
    shared.set_digital_output_pin_mode(shared.digitPins)

"""
Function to clear all arduino pins - pins are cleared then and there after outputs but do this to make sure they are all clear when system shuts down
Params: None
Return: None
"""
def clear_pins():
    print("Cleaning system...\n")
    # digital output pins
    pinList = [
        shared.redLEDPin, 
        shared.blueLEDPin, 
        shared.lowLEDPin, 
        shared.highLEDPin, 
        shared.flashingLEDPin, 
        shared.pinSER1, 
        shared.pinSRCLK1, 
        shared.pinRCLK1, 
        shared.pinSER2, 
        shared.pinSRCLK2, 
        shared.pinRCLK2, 
        shared.buzzerPin1, 
        shared.buzzerPin2
    ]
    for pin in pinList:
        shared.board.digital_write(pin, 0)

if __name__ == "__main__":
    main()
