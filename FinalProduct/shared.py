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
# constants
PIN = 1234
# for 8 segment display -> # a-g not including dp
CHAR_MAP = {
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
TEMP_MAP = {
    0: [1, 0, 0, 0, 0, 0, 0, 0],
    1: [1, 1, 0, 0, 0, 0, 0, 0],
    2: [1, 1, 1, 0, 0, 0, 0, 0],
    3: [1, 1, 1, 1, 0, 0, 0, 0],
    4: [1, 1, 1, 1, 1, 0, 0, 0],
    5: [1, 1, 1, 1, 1, 1, 0, 0],
    6: [1, 1, 1, 1, 1, 1, 1, 0],
    7: [1, 1, 1, 1, 1, 1, 1, 1],
}
# reference values
minLowTemp = 20
maxHighTemp = 25
desiredTimeoutDuration = 120
# user modifiable params
ambientTempHigh = 25
ambientTempLow = 20
systemSettingsAccessDuration = 120 # admin access timeout duration
# tolerences
temperatureTolerence = 1 # value by which the temperature thresholds can vary in C
accessDurationTolerence = 10 # # value by which the system settings access duration can vary in s
doorTolerence = 2 # tolerence level for closed door measurement in cm
lightTolerence = 50 # tolerence level for ambient lighting in voltage units
# other global vars
board = pymata4.Pymata4() # arduino board instance
invalidPINTimeoutStart = 0 # start time for system lock due to invalid PIN
systemSettingsStartTime = 0 # start time for system settings access
mode = 0 # 1 if heating -1 if cooling 0 if neither
outsideTemperature = 0 # temperature outside the model room in C
closedDoorDistance = 0 # distance to the door from sonar sensor when closed in cm
ambientLightLevel = 0 # ambient light level in the room in voltage units
isLightingNotAmbient = 0 # identif if lighting inside the room is ambient
isDoorOpen = 0 # closed/ open status of the door -> 0 means closed
# data stores
temperatureMap = [] # list of tempratures and their recorded times for the last 20s -> to be used for graphing
lightIntensityMap = [] # list of light intensity value and their recorded times for the last 20s -> to be used for graphing
systemModeMap = []  # list of system mode values and their recorded times for the last 20s -> to be used for graphing
# digital input pins
pushButtonPin = 9 # digital push button pin
triggerPin = 10 # digital ultrasonic trigger pin
echoPin = 11 # digital ultrasonic echo pin
# analog input pins
thermistorPinIn = 0 # analog thermistor pin inside
thermistorPinOut = 1 # # analog thermistor pin outside
ldrPin = 1 # analog LDR pin
# digital output pins
redLEDPin = 2
blueLEDPin = 3
lowLEDPin = 4
highLEDPin = 5
flashingLEDPin = 6
ultrasonicResponsePin = 1
ldrResponsePin = 2
pinSER1 = 5
pinSRCLK1 = 6
pinRCLK1 = 7
pinSER2 = 5
pinSRCLK2 = 6 
pinRCLK2 = 7
pinSER3 = 7
pinSRCLK3 = 8 
pinRCLK3 = 9
buzzerPin1 = 7
buzzerPin2 = 8
digitPins = [8, 9, 10, 11]

"""
Function to set pin mode of digital output pins
Params: pinList     -> list of pins to be set as digital outputs
Return: None
"""
def set_digital_output_pin_mode(pinList):
    for pin in pinList:
        board.set_pin_mode_digital_output(pin)

"""
Function to set pin mode of digital input pins
Params: pinList     -> list of pins to be set as digital inputs
Return: None
"""
def set_digital_input_pin_mode(pinList):
    for pin in pinList:
        board.set_pin_mode_digital_input(pin) 

"""
Function to set pin mode of analog input pins
Params: pinList     -> list of pins to be set as analog inputs
Return: None
"""
def set_analog_input_pin_mode(pinList):
    for pin in pinList:
        board.set_pin_mode_analog_input(pin)

"""
Function to set pin mode of sonar pins
Params: pinList     -> in the order of trigger pin, echo pin
Return: None
"""
def set_sonar_input_pin_mode(pinList):
    board.set_pin_mode_sonar(pinList[0], pinList[1]) 