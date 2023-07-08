"""
Project:        ENG1013 HVAC
File:           controlSystem.py
Purpose:        This file contains the invocation of the polling loop/ fan operation of the HVAC
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from inputs import calibrateSonarSensor, calibrateLDRSensor, checkTemperature, isSwitchMode, checkRoomDoor, checkRoomLighting
from outputs import controlRoomEnvironment, forceControlLEDs
import shared
import time
import sys

# global vars

"""
Function to initiate the control system
Params: None
Return: None
"""
def controlSystem():
    try:
        # calibrate sensors before starting the polling loop - only needed to be done at the beginning of the control system
        print("Calibrating sensors. Please make sure the door is closed and lighting is normal...\n")
        # calibrate sonar sensor
        calibrateSonarSensor()
        # calibrate LDR sensor
        calibrateLDRSensor()

        # start polling loop
        print("Starting polling loop...\n")
        startPollingLoop()
    except KeyboardInterrupt:
        print("\nExiting control system...")
        # TODO: turn off all control system outputs before shutting down the board
        # shared.board.shutdown() - DO NOT shut the board down here, will affect graphing
        return
 
"""
Function to run the polling loop for fan operation
Params: None
Return: None
"""
def startPollingLoop():
    while True:
        startLoop = time.time() # record loop start time
        
        # read temperature outside the room and record the ambient temprature
        shared.outsideTemperature, _ = checkTemperature(0) 

        # read temperature inside the room
        currTemp, currTime = checkTemperature(1)
        prevTemp = currTemp if len(shared.temperatureMap) == 0 else shared.temperatureMap[-1][1] # get last recorded temperature. if array is empty, use current value

        # adjust stored temperature data
        while (len(shared.temperatureMap) != 0) and ((currTime - shared.temperatureMap[0][0]) > 20): # only keep the temperature data from last 20s
            shared.temperatureMap.pop(0)
        shared.temperatureMap.append((currTime, currTemp))

        # calculate trend (increasing/ decreasing/ constant)
        trend = 1 if currTemp - prevTemp > 0 else -1 if currTemp - prevTemp < 0 else 0 # check if the temperature is increasing/ decreasing or constant
        
        # TODO: display temprature on the thermometer

        # TODO: display temprature on the 7 seg - 4 digit alpha-numeric without scrolling

        # control fans (LEDs) based on the temperature
        controlRoomEnvironment(currTemp, trend)

        # check for fan operation (LED) mode change trigger - ideally should be setup as an interrupt
        if (isSwitchMode()): # if push button pressed, switch current mode
            shared.mode = not (shared.mode)
            forceControlLEDs()

        # check if the room door is open - ideally should be setup as an interrupt
        currDist, _ = checkRoomDoor()
        if (currDist > (shared.closedDoorDistance + shared.doorTolerence)): # door is open
            pass

        # check if the lighting in the room changed - ideally should be setup as an interrupt
        currLightLevel, _ = checkRoomLighting()
        if (currLightLevel > (shared.ambientLightLevel + shared.lightTolerence)): # lighting increased inside the room
            pass
        elif (currLightLevel < (shared.ambientLightLevel - shared.lightTolerence)): # lighting decreased inside the room
            pass

        endLoop = time.time() # record loop end time
        print(f"\nTime taken by the polling loop: {endLoop - startLoop}")