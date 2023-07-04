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
# board = pymata4.Pymata4() # arduino board instance
ambientTempHigh = 25
ambientTempLow = 20
temperatureMap = [] # list of tempratures and their recorded times for the last 20s -> to be used for graphing
