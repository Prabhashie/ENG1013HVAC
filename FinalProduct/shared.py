"""
Project:        ENG1013 HVAC
File:           shared.py
Purpose:        This file contains the shared variables across all files
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from pymata4 import pymata4

# global vars
PIN = 1234
board = pymata4.Pymata4() # arduino board instance
temperatureTolerence = 0 # ambient temperatured will be measured using the 2nd thermistor
# ambient temperature to be decided by +/- diff values
ambientTempHigh = 25
ambientTempLow = 20
outsideTemperature = 0 # temperature outside the model room in C
# TODO: Other user modifiable parameters
temperatureMap = [] # list of tempratures and their recorded times for the last 20s -> to be used for graphing
# for 8 segment display -> # a-g,dp
alphabet = {
    "A": int("11101110", 2),
    "B": int("00111110", 2),
    "C": int("10011100", 2),
    "D": int("01111010", 2),
    "E": int("10011110", 2),
    "F": int("10001110", 2),
    "G": int("10111100", 2),
    "H": int("01101110", 2),
    "I": int("10001000", 2),
    "J": int("01110000", 2),
    "K": int("10101110", 2),
    "L": int("00011100", 2),
    "M": int("10101010", 2),
    "N": int("00101010", 2),
    "O": int("00111010", 2),
    "P": int("11001110", 2),
    "Q": int("11100110", 2),
    "R": int("00001010", 2),
    "S": int("10110110", 2),
    "T": int("00011110", 2),
    "U": int("00111000", 2),
    "V": int("01111100", 2),
    "W": int("01010110", 2),
    "X": int("01101110", 2),
    "Y": int("01110110", 2),
    "Z": int("11010010", 2),
    "0": int("11111100", 2),
    "1": int("01100000", 2),
    "2": int("11011010", 2),
    "3": int("11110010", 2),
    "4": int("01100110", 2),
    "5": int("10110110", 2),
    "6": int("10111110", 2),
    "7": int("11100000", 2),
    "8": int("11111110", 2),
    "9": int("11110110", 2),
}
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
PIN_MASK = 0b10000000
invalidPINTimeoutStart = 0 # start time for system lock due to invalid PIN
systemSettingsStartTime = 0 # start time for system settings access
systemSettingsAccessDuration = 120 # admin access timeout duration
mode = 1 # 1 if heating 0 if cooling
closedDoorDistance = 0 # distance to the door from sonar sensor when closed in cm
doorTolerence = 2 # tolerence level for closed door measurement in cm
ambientLightLevel = 0 # ambient light level in the room in voltage units
lightTolerence = 50 # tolerence level for ambient lighting in voltage units

"""
Function to set pin mode of digital output pins
Params: pinList     -> list of pins to be set as digital outputs
Return: None
"""
def setDigitalOutputPinMode(pinList):
    for pin in pinList:
        board.set_pin_mode_digital_output(pin)

"""
Function to set pin mode of digital input pins
Params: pinList     -> list of pins to be set as digital inputs
Return: None
"""
def setDigitalInputPinMode(pinList):
    for pin in pinList:
        board.set_pin_mode_digital_input(pin) 

"""
Function to set pin mode of analog input pins
Params: pinList     -> list of pins to be set as analog inputs
Return: None
"""
def setAnalogInputPinMode(pinList):
    for pin in pinList:
        board.set_pin_mode_analog_input(pin)

"""
Function to set pin mode of sonar pins
Params: pinList     -> in the order of trigger pin, echo pin
Return: None
"""
def setSonarInputPinMode(pinList):
    board.set_pin_mode_sonar(pinList[0], pinList[1]) 