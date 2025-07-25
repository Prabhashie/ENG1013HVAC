"""
Project:        ENG1013 HVAC
File:           inputs.py
Purpose:        This file reads the voltage measurement across a thermistor and calculates the temperature
Authors:        Sachinthana Pathiranage, Erim Can
Date Created:   04/07/2023
"""

# imports
import shared
import math
import time

# global vars

vIn = 5 # input voltage in Volts
r1 = 100000 # known resistance value in Ohms - use 10k or 100k as the thermistor is 10k at 25C (https://forum.arduino.cc/t/thermistor-reading-incorrectly/343362/5)
# steinhart - hart coefficients
c1 = 1.009249522e-03
c2 = 2.378405444e-04
c3 = 2.019202697e-07

"""
Function to obtain average temperature reading over 1 second
Params: selector    -> selects which thermistor to read. 0 for outside and 1 for inside
Return: tempReading -> average temperature value over 1s
        time        -> current time
"""
def check_temperature(selector):
    # pin mode set during system initialization
    if selector: 
        thermistorLocation = "inside"
    else:
        thermistorLocation = "outside"

    startTime = time.time()
    currTime = time.time()
    tempVals = []

    while (currTime - startTime < 1): # record temperatures continuously for 1s
        calculate_temp(selector, tempVals)
        currTime = time.time()
    
    # filter/ average temperature values by averaging readings in the array
    tempReading = round(sum(tempVals)/ len(tempVals), 1) # temperature stored every 1s
    print(f"Current temperature {thermistorLocation} the room is {tempReading} C")
    return tempReading, time.time()

"""
Function to calulate temperature from thermistor voltage reading
Params: selector    -> selects which thermistor to read. 0 for outside and 1 for inside
        tempVals    -> array to store temperature values
Return: None
"""
def calculate_temp(selector, tempVals):
    time.sleep(0.01) # check this time value
    if selector:
        thermistorPinReading, _ = shared.board.analog_read(shared.thermistorPinIn)
    else:
        thermistorPinReading, _ = shared.board.analog_read(shared.thermistorPinOut)
    vOut = (vIn / 1023) * thermistorPinReading
    r2 = r1 * ((vIn/vOut) - 1)
    logR2 = math.log(r2)
    tF = (1.0 / (c1 + c2*logR2 + c3*logR2**3)) # temperature in Fahrenheit 
    tC = tF - 273.15 # temperature in Calcius
    tempVals.append(tC)

"""
Function to read push button input - when pressed switches from cooling to heating mode and vice versa (https://www.instructables.com/Understanding-the-Pull-up-Resistor-With-Arduino/)
Params: None
Return: True/ False -> if mode should be switched or not
"""
def is_switch_mode(): # ideally the push button press should generate an interrupt, but we do not use async calls in the scope of the unit
    print("Reading push button input...")
    # pin mode set during system initialization
    readings = []
    for _ in range(10):
        readings.append(shared.board.digital_read(shared.pushButtonPin)[0])
    if sum(readings)/ len(readings) >= 0.5: # switch the mode if button pressed
        print(f"{readings}")
        return True
    return False

"""
Function to read ultrasonic sensor - detect if the room door is open (https://www.instructables.com/Distance-Sensor-Instructable/, 
                                                                        https://www.youtube.com/watch?v=n_lZCIA25aI&ab_channel=RealPars,
                                                                        https://learn.adafruit.com/calibrating-sensors?view=all)
Params: None
Return: distReading -> average distance to the door reading over 1s
        time        -> current time
"""
def check_room_door():
    # pin mode set during system initialization
    # read the sensor
    startTime = time.time()
    currTime = time.time()
    distVals = []

    while (currTime - startTime < 1): # record distance continuously for 1s
        calculate_distance(distVals)
        currTime = time.time()
    
    # filter/ average distance values by averaging readings in the array
    distReading = round(sum(distVals)/ len(distVals), 0) # distance stored every 1s
    print(f"Current distance to the door is {distReading} cm")
    return distReading, time.time()

"""
Function to calulate the distance from sonar sensor
Params: distVals    -> array to store distance values
Return: None
"""
def calculate_distance(distVals):
    time.sleep(0.01)
    # if callback used, it will receive data every time the SENSOR VALUE CHANGES (https://mryslab.github.io/pymata4/pin_modes/)
    # if the sensor is manually read/ polled as below, will get readings everytime polled, despite the sensor value changed or not
    sonarPinReading, _ = shared.board.sonar_read(shared.triggerPin) 
    distVals.append(sonarPinReading) # distances are in cm

"""
Function to read LDR sensor - detect if the room lighting has changed
Params: None
Return: voltageReading  -> average voltage reading corrsponding to the room light level over 1s
        time            -> current time
"""
def check_room_lighting():
    # pin mode set during system initialization
    # read the sensor
    startTime = time.time()
    currTime = time.time()
    voltageVals = []

    while (currTime - startTime < 1): # record light level continuously for 1s
        calculate_lighting(voltageVals)
        currTime = time.time()
    
    # filter/ average voltage values by averaging readings in the array
    voltageReading = round(sum(voltageVals)/ len(voltageVals), 0) # light level stored every 1s
    print(f"Current light level in the room is {voltageReading} voltage units")
    return voltageReading, time.time()

"""
Function to calulate the distance from sonar sensor
Params: tempVals    -> array to store temperature values
Return: None
"""
def calculate_lighting(voltageVals):
    time.sleep(0.01)
    ldrPinReading, _ = shared.board.analog_read(shared.ldrPin) 
    voltageVals.append(ldrPinReading) # voltage values are in voltage units

"""
Function to calibrate the sonar sensor
    - place the sensor inside the room
    - close the door
    - take readings for some time to identify distance to the door when sufficiently closed
    - use this as the reference/ closed door distance 
Params: None
Return: None
"""  
def calibrate_sonar_sensor(): # identify the distance to the door when sufficiently closed
    # pin mode set during system initialization
    distVals = []
    for _ in range(10):
        time.sleep(0.01)
        distVals.append(shared.board.sonar_read(shared.triggerPin)[0])
    shared.closedDoorDistance = sum(distVals)/ len(distVals)

"""
Function to calibrate the LDR sensor
    - place the sensor inside the room
    - close the door
    - lighting should be normal
    - take readings for some time to identify the light levels for ambient settings
    - use this as the reference for ambient lighting
    - light increases -> resistance decreases -> voltage decreases
    - https://www.instructables.com/Arduino-and-a-LDR-Light-Dependent-Resistor/
    - https://kitronik.co.uk/blogs/resources/how-an-ldr-light-dependent-resistor-works
Params: None
Return: None
"""
def calibrate_ldr_sensor(): # identify the distance to the door when sufficiently closed
    # pin mode set during system initialization
    voltageVals = []
    for _ in range(10): # record the voltage across the LDR whe there's ambient lighting
        time.sleep(0.01)
        voltageVals.append(shared.board.analog_read(shared.ldrPin)[0])
    shared.ambientLightLevel = sum(voltageVals)/ len(voltageVals)