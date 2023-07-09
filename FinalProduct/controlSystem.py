"""
Project:        ENG1013 HVAC
File:           controlSystem.py
Purpose:        This file contains the invocation of the polling loop/ fan operation of the HVAC
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from inputs import calibrate_sonar_sensor, calibrate_ldr_sensor, check_temperature, is_switch_mode, check_room_door, check_room_lighting
from outputs import control_room_environment, force_control_leds, display_four_character_string, alert_change
import shared
import time
import sys

# global vars

"""
Function to initiate the control system
Params: None
Return: None
"""
def control_system():
    try:
        # calibrate sensors before starting the polling loop - only needed to be done at the beginning of the control system
        print("Calibrating sensors. Please make sure the door is closed and lighting is normal...\n")
        # calibrate sonar sensor
        calibrate_sonar_sensor()
        # calibrate LDR sensor
        calibrate_ldr_sensor()

        # start polling loop
        print("Starting polling loop...\n")
        start_polling_loop()
    except KeyboardInterrupt:
        print("\nExiting control system...")
        # TODO: turn off all control system outputs (except 7 seg) before shutting down the board - 7 seg used in main
        # shared.board.shutdown() - DO NOT shut the board down here, will affect graphing
        return
 
"""
Function to run the polling loop for fan operation
Params: None
Return: None
"""
def start_polling_loop():
    while True:
        startLoop = time.time() # record loop start time
        
        # read temperature outside the room and record the ambient temprature
        shared.outsideTemperature, _ = check_temperature(0) 

        # read temperature inside the room
        currTemp, currTime = check_temperature(1)
        prevTemp = currTemp if len(shared.temperatureMap) == 0 else shared.temperatureMap[-1][1] # get last recorded temperature. if array is empty, use current value

        # adjust stored temperature data
        while (len(shared.temperatureMap) != 0) and ((currTime - shared.temperatureMap[0][0]) > 20): # only keep the temperature data from last 20s
            shared.temperatureMap.pop(0)
        shared.temperatureMap.append((currTime, currTemp))

        # calculate trend (increasing/ decreasing/ constant)
        trend = 1 if currTemp > prevTemp else -1 if currTemp < prevTemp else 0 # check if the temperature is increasing/ decreasing or constant
        
        # TODO: display temprature on the thermometer
        
        # display temprature on the 7 seg - 4 digit alpha-numeric without scrolling
        string = str(int(currTemp))
        duration = 1 # display for 1s
        display_four_character_string(string, duration)

        # control fans (LEDs) based on the temperature
        control_room_environment(currTemp, trend)

        # alert about change in temperature
        alert_change(trend)

        # check for fan operation (LED) mode change trigger - ideally should be setup as an interrupt
        if (is_switch_mode() and not shared.mode): # if push button pressed, switch current mode
            shared.mode = shared.mode * -1
            shared.systemModeMap.append((time.time(), shared.mode))
            force_control_leds()

        # check if the room door is open - ideally should be setup as an interrupt
        currDist, currTime = check_room_door()
        if (currDist > (shared.closedDoorDistance + shared.doorTolerence)): # door is open
            pass

        # check if the lighting in the room changed - ideally should be setup as an interrupt
        currLightLevel, currTime = check_room_lighting()
        
        # adjust stored light intensity data
        while (len(shared.lightIntensityMap) != 0) and ((currTime - shared.lightIntensityMap[0][0]) > 20): # only keep the temperature data from last 20s
            shared.lightIntensityMap.pop(0)
        # convert light intensity to voltage
        currLightLevelVolts = (currLightLevel / 1023) * 5 # input voltage is taken as 5V
        shared.lightIntensityMap.append((currTime, currLightLevelVolts))

        if (currLightLevel > (shared.ambientLightLevel + shared.lightTolerence)): # lighting increased inside the room
            pass
        elif (currLightLevel < (shared.ambientLightLevel - shared.lightTolerence)): # lighting decreased inside the room
            pass
        
        # adjust stored mode data
        while (len(shared.systemModeMap) != 0) and ((shared.systemModeMap[-1][0] - shared.systemModeMap[0][0]) > 20): # only keep the temperature data from last 20s
            shared.systemModeMap.pop(0)
        
        endLoop = time.time() # record loop end time
        print(f"\nTime taken by the polling loop: {endLoop - startLoop}")