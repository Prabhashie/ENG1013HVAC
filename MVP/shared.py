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