"""
Project:        ENG1013 HVAC
File:           controlSystem.py
Purpose:        This file contains the invocation of the polling loop/ fan operation of the HVAC
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from inputs import calibrateSonarSensor, calibrateLDRSensor, checkTemperature, isSwitchMode, checkRoomDoor
from outputs import displayTemp, forceControlLEDs
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
        shared.board.shutdown()
        return
 
"""
Function to run the polling loop for fan operation
Params: None
Return: None
"""
def startPollingLoop():
    while True:
        startLoop = time.time() # record loop start time

        # read temperature inside the room
        currTemp, currTime = checkTemperature()
        prevTemp = currTemp if len(shared.temperatureMap) == 0 else shared.temperatureMap[-1][1] # get last recorded temperature. if array is empty, use current value

        # adjust stored temperature data
        while (len(shared.temperatureMap) != 0) and ((currTime - shared.temperatureMap[0][0]) > 20): # only keep the temperature data from last 20s
            shared.temperatureMap.pop(0)
        shared.temperatureMap.append((currTime, currTemp))

        # calculate trend (increasing/ decreasing/ constant)
        trend = 1 if currTemp - prevTemp > 0 else -1 if currTemp - prevTemp < 0 else 0 # check if the temperature is increasing/ decreasing or constant
        
        # control fan (LEDs) based on the temperature
        displayTemp(currTemp, trend)

        # check for fan operation (LED) mode change trigger - ideally should be setup as an interrupt
        if (isSwitchMode()): # if push button pressed, switch current mode
            shared.mode = not (shared.mode)
            forceControlLEDs()

        # check if the room door is open - ideally should be setup as an interrupt
        currDist, _ = checkRoomDoor()
        if (currDist > shared.closedDoorDistance): # door is open
            pass

        # check if the lighting in the room changed - ideally should be setup as an interrupt

        endLoop = time.time() # record loop end time
        print(f"\nTime taken by the polling loop: {endLoop - startLoop}")