"""
Project:        ENG1013 HVAC
File:           inputs.py
Purpose:        This file reads the voltage measurement across a thermistor and calculates the temperature
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from shared import *
import math
import time

# global vars
thermistorPin = 0 # analog thermistor pin
vIn = 5 # input voltage in Volts
r1 = 100000 # known resistance value in Ohms
# steinhart - hart coefficients
c1 = 1.009249522e-03
c2 = 2.378405444e-04
c3 = 2.019202697e-07

"""
Function to obtain average temperature reading over 3 seconds
Params: None
Return: tempReading -> Average temperature value over 3s
"""
def readThermistor():
    setAnalogInputPinMode([thermistorPin]) # callback function not set as temperature values are averaged over time
    startTime = time.time()
    currTime = time.time()
    tempVals = []

    while (currTime - startTime < 3): # record temperatures continuously for 3s
        calculateTemp(tempVals)
        currTime = time.time()
    
    # filter/ average temperature values by averaging readings in the array
    tempReading = sum(tempVals)/ len(tempVals) # temperature stored every 3s
    print(f"Current Temperature is {tempReading} C")
    return tempReading, time.time()

"""
Function to calulate temperature from thermistor voltage reading
Params: tempVals    -> array to store temperature values
Return: None
"""
def calculateTemp(tempVals):
    time.sleep(0.05)
    thermistorPinReading, _ = board.analog_read(thermistorPin)
    vOut = (vIn / 1023) * thermistorPinReading
    r2 = r1 * ((vIn/vOut) - 1)
    logR2 = math.log(r2)
    tF = (1.0 / (c1 + c2*logR2 + c3*logR2**3)) # temperature in Fahrenheit 
    tC = tF - 273.15 # temperature in Calcius
    tempVals.append(tC)

# TODO: read push buttons

# TODO: read ultra-sonic sensor
    # calibration
    # filter -> 1s
# TODO: read LDR
    # calibration
    # filter -> 1s