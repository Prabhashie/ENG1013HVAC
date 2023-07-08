"""
Project:        ENG1013 HVAC
File:           graphing.py
Purpose:        This file handles the graph operations of the system
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
from shared import *
from matplotlib import pyplot
import sys
from datetime import datetime

# global vars

"""
Function to produce graphs
Params: None
Return: None
"""
def graphing():
    # loop if an incorrect input is entered
    while True:
        print("Please select from the below options: \n1. Temperature Vs. Time \n2. Light Intensity Vs. Time \n3. Fan Mode Vs. Time \n") 
        try:
            userInput = int(input("Your Choice: "))
            if (userInput not in [1,2,3]):
                print("Invalid selection! Please choose again.\n")
                continue
        except ValueError:
            print("Please enter a value between 1 and 3.\n")
        except KeyboardInterrupt:
            print("\nExiting system...\n")
            return

        # call relavent function
        if userInput == 1:
            graph_temp_vs_time()
        elif userInput == 2:
            graph_light_intensity_vs_time()
        elif userInput == 3:
            graph_fan_mode_vs_time()
    
"""
Function to plot temperature vs time graph
Params: None
Return: None
"""
def graph_temp_vs_time():
    timeData = []
    temperatureData = []
    for item in temperatureMap:
        timeData.append(item[0] - temperatureMap[0][0]) # display the time axis between 0-20s
        temperatureData.append(item[1])
    print("Graphing variation of temperature over past 20s...")
    pyplot.plot(timeData, temperatureData, "*")
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Temperature (C)')
    pyplot.xlim([0, 20])
    pyplot.title("Temperature variation inside the room within the last 20s")
    pyplot.savefig(f'results/TempVsTime_{datetime.now().strftime("%Y%m%d%H%M%S")}.png') # https://mljar.com/blog/matplotlib-save-plot/
    pyplot.show()

"""
Function to plot light intensity vs time graph
Params: None
Return: None
"""
def graph_light_intensity_vs_time():
    timeData = []
    lightIntensityData = []
    for item in lightIntensityMap:
        timeData.append(item[0] - lightIntensityMap[0][0])
        lightIntensityData.append(item[1])
    print("Graphing variation of light intensity over past 20s...")
    pyplot.plot(timeData, lightIntensityData, "*")
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('Light intensity (V)')
    pyplot.xlim([0, 20])
    pyplot.title("Light intensity variation inside the room within the last 20s")
    pyplot.savefig(f'results/LightVsTime_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')
    pyplot.show()

"""
Function to plot fan mode vs time graph
Params: None
Return: None
"""
def graph_fan_mode_vs_time():
    timeData = []
    modeData = []
    for item in systemModeMap:
        timeData.append(item[0] - systemModeMap[0][0])
        modeData.append(item[1])
    if len(systemModeMap) == 0: # if mode didn't change over the last 20s
        timeData = [i for i in range(20)]
        modeData = [0] * 20
    print("Graphing variation of system mode over past 20s...")
    pyplot.plot(timeData, modeData, "*")
    pyplot.xlabel('Time (s)')
    pyplot.ylabel('System mode')
    pyplot.xlim([0, 20])
    pyplot.title("System mode variation inside the room within the last 20s")
    pyplot.savefig(f'results/ModeVsTime_{datetime.now().strftime("%Y%m%d%H%M%S")}.png')
    pyplot.show()