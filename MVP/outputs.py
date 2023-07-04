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
    pass

def controlLEDs():
    pass

def printToConsole():
    pass