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
ambientTempHigh = 25
ambientTempLow = 20
temperatureMap = [(1,2),(2,3),(3,4)] # list of tempratures and their recorded times for the last 20s -> to be used for graphing
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
PIN_MASK = 0b10000000
invalidPINTimeoutStart = 0 # start time for system lock due to invalid PIN
systemSettingsStartTime = 0 # start time for system settings access
systemSettingsAccessDuration = 120 # admin access timeout duration

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