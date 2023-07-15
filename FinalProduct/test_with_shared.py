import shared
import time
import sys
import math

"""
''' VERY VERY VERY IMPORTANT: CONNECT PINS AS GIVEN IN https://docs.arduino.cc/tutorials/communication/guide-to-shift-out '''

shared.pinSER1 = 8
shared.pinSRCLK1 = 9
shared.pinRCLK1 = 10
shared.digitPins = [4, 5, 6, 7]
shared.CHAR_MAP = {
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

shared.set_digital_output_pin_mode([shared.pinSER1, shared.pinSRCLK1, shared.pinRCLK1])
shared.set_digital_output_pin_mode(shared.digitPins)

def display_character(character, digit):

    segments = shared.CHAR_MAP[character]
    for i in shared.digitPins:
        shared.board.digital_write(i, 1) # turn off all digits
    for _ in range(8): # clear all the segments and turn off
        shared.board.digital_write(shared.pinSER1, 0)
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)

    shared.board.digital_write(shared.pinRCLK1, 1)
    shared.board.digital_write(shared.pinRCLK1, 0)
    
    # pins should be written g - a
    # connect the shift reg to the 7 seg accordingly
    for i in range(6, -1, -1): # write value to the 7 seg
        shared.board.digital_write(shared.pinSER1, segments[i])
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)
   
    shared.board.digital_write(shared.pinRCLK1, 1)
    shared.board.digital_write(shared.pinRCLK1, 0)
    
    shared.board.digital_write(shared.digitPins[digit - 1], 0) # turn on the digit pin
    time.sleep(5)

display_character("5", 2)
shared.board.shutdown()
sys.exit(0)
"""

"""
''' VERY VERY VERY IMPORTANT: CONNECT PINS AS GIVEN IN https://docs.arduino.cc/tutorials/communication/guide-to-shift-out '''

shared.pinSER2 = 8
shared.pinSRCLK2 = 9
shared.pinRCLK2 = 10
shared.TEMP_MAP = {
    0: [1, 0, 0, 0, 0, 0, 0, 0],
    1: [1, 1, 0, 0, 0, 0, 0, 0],
    2: [1, 1, 1, 0, 0, 0, 0, 0],
    3: [1, 1, 1, 1, 0, 0, 0, 0],
    4: [1, 1, 1, 1, 1, 0, 0, 0],
    5: [1, 1, 1, 1, 1, 1, 0, 0],
    6: [1, 1, 1, 1, 1, 1, 1, 0],
    7: [1, 1, 1, 1, 1, 1, 1, 1],
}

shared.set_digital_output_pin_mode([shared.pinSER2, shared.pinSRCLK2, shared.pinRCLK2])

def display_temeprature(temp):
    # pin mode set during system initialization
    if temp < 18:
        code = shared.TEMP_MAP[0]
    elif 18 <= temp < 20:
        code = shared.TEMP_MAP[1]
    elif 20 <= temp < 22:
        code = shared.TEMP_MAP[2]
    elif 22 <= temp < 24:
        code = shared.TEMP_MAP[3]
    elif 24 <= temp < 26:
        code = shared.TEMP_MAP[4]
    elif 26 <= temp < 28:
        code = shared.TEMP_MAP[5]
    elif 28 <= temp < 30:
        code = shared.TEMP_MAP[6]
    else:
        code = shared.TEMP_MAP[7]

    for _ in range(8):
        shared.board.digital_write(shared.pinSER2, 0)
        shared.board.digital_write(shared.pinSRCLK2, 1)
        shared.board.digital_write(shared.pinSRCLK2, 0)

    shared.board.digital_write(shared.pinRCLK2, 1)
    shared.board.digital_write(shared.pinRCLK2, 0)
    
    for i in range(8):
        shared.board.digital_write(shared.pinSER2, code[i])
        shared.board.digital_write(shared.pinSRCLK2, 1)
        shared.board.digital_write(shared.pinSRCLK2, 0)

    shared.board.digital_write(shared.pinRCLK2, 1)
    shared.board.digital_write(shared.pinRCLK2, 0)

    time.sleep(5)

display_temeprature(35)
shared.board.shutdown()
sys.exit(0)
"""

"""
''' https://docs.arduino.cc/built-in-examples/digital/Button '''

shared.mode = 1
shared.pushButtonPin = 2
# shared.redPin = 8
# shared.bluePin = 9

shared.set_digital_input_pin_mode([shared.pushButtonPin])
# shared.set_digital_output_pin_mode([shared.redPin, shared.bluePin])

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

for i in range(100):
    print(f"i = {i}")
    time.sleep(2)
    if (is_switch_mode() and shared.mode): # if push button pressed, switch current mode
        shared.mode = shared.mode * (-1)
        if shared.mode == 1:
            # shared.board.digital_write(shared.bluePin, 0)
            # shared.board.digital_write(shared.redPin, 1)
            print("Red On")
            time.sleep(2)
            
        else:
            # shared.board.digital_write(shared.redPin, 0)
            # shared.board.digital_write(shared.bluePin, 1)
            print("Blue On")
            time.sleep(2)

shared.board.shutdown()
sys.exit(0)
"""

"""
shared.set_digital_output_pin_mode([shared.pinSER1, shared.pinSRCLK1, shared.pinRCLK1])
def display_character(character, digit):
    # pin mode set during system initialization
    segments = shared.CHAR_MAP[character]
    for _ in range(8): # turn off all digits
        shared.board.digital_write(shared.pinSER1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0) 
    for _ in range(8): # clear all the segments and turn off
        shared.board.digital_write(shared.pinSER1, 0)
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)

    shared.board.digital_write(shared.pinRCLK1, 1)
    shared.board.digital_write(shared.pinRCLK1, 0)

    # pins should be written 1 - 4
    # connect the shift reg to the 7 seg accordingly
    digits = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    digits[digit - 1] = 0 # turn on the digit pin
    for i in range(8):
        shared.board.digital_write(shared.pinSER1, digits[i])
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)
    
    # write to dp
    shared.board.digital_write(shared.pinSER1, 0)
    shared.board.digital_write(shared.pinSRCLK1, 1)
    shared.board.digital_write(shared.pinSRCLK1, 0)
    # pins should be written g - a
    # connect the shift reg to the 7 seg accordingly
    for i in range(6, -1, -1): # write value to the 7 seg
        shared.board.digital_write(shared.pinSER1, segments[i])
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)
    # write to dp
    # shared.board.digital_write(shared.pinSER1, 0)
    # shared.board.digital_write(shared.pinSRCLK1, 1)
    # shared.board.digital_write(shared.pinSRCLK1, 0)
   
    shared.board.digital_write(shared.pinRCLK1, 1)
    shared.board.digital_write(shared.pinRCLK1, 0)

    time.sleep(0.025)
def display_four_character_string(string, duration):
    # pin mode set during system initialization
    string = string.upper() # turn the string to all upper case
    fourCharacterStartTime = time.time()
    while time.time() - fourCharacterStartTime < duration:
        for i in range(4):
            display_character(string[i], i+1)

    # clear output pins
    for _ in range(4): # turn off all digits
        shared.board.digital_write(shared.pinSER1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)  
    for _ in range(8): # turn off all digits - can use CLR pin in the shift reg at the cost of an additional arduino pin
        shared.board.digital_write(shared.pinSER1, 0)
        shared.board.digital_write(shared.pinSRCLK1, 1)
        shared.board.digital_write(shared.pinSRCLK1, 0)

    shared.board.digital_write(shared.pinRCLK1, 1)
    shared.board.digital_write(shared.pinRCLK1, 0)

display_four_character_string("TEST", 5)
shared.board.shutdown()
sys.exit(0)
"""

"""
vIn = 5 # input voltage in Volts
r1 = 220 # known resistance value in Ohms
# steinhart - hart coefficients
c1 = 1.009249522e-03
c2 = 2.378405444e-04
c3 = 2.019202697e-07

shared.set_analog_input_pin_mode([shared.thermistorPinIn, shared.thermistorPinOut])

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

def calculate_temp(selector, tempVals):
    time.sleep(0.05) # check this time value
    if selector:
        thermistorPinReading, _ = shared.board.analog_read(shared.thermistorPinIn)
    else:
        thermistorPinReading, _ = shared.board.analog_read(shared.thermistorPinOut)
    print(thermistorPinReading)
    vOut = (vIn / 1023) * thermistorPinReading
    r2 = r1 * ((vIn/vOut) - 1)
    logR2 = math.log(r2)
    tF = (1.0 / (c1 + c2*logR2 + c3*logR2**3)) # temperature in Fahrenheit 
    tC = tF - 273.15 # temperature in Calcius
    tempVals.append(tC)

check_temperature(0)
time.sleep(2)
check_temperature(0)
shared.board.shutdown()
sys.exit(0)
"""
