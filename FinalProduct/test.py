import time
import sys
from pymata4 import pymata4

"""
''' VERY VERY VERY IMPORTANT: CONNECT PINS AS GIVEN IN https://docs.arduino.cc/tutorials/communication/guide-to-shift-out '''

pinSER1 = 8
pinSRCLK1 = 9
pinRCLK1 = 10
digitPins = [4, 5, 6, 7]
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

board = pymata4.Pymata4()
board.set_pin_mode_digital_output(pinSER1)
board.set_pin_mode_digital_output(pinSRCLK1)
board.set_pin_mode_digital_output(pinRCLK1)
for pin in digitPins:
    board.set_pin_mode_digital_output(pin)

def display_character(character, digit):

    segments = CHAR_MAP[character]
    for i in digitPins:
        board.digital_write(i, 1) # turn off all digits
    for _ in range(8): # clear all the segments and turn off
        board.digital_write(pinSER1, 0)
        board.digital_write(pinSRCLK1, 1)
        board.digital_write(pinSRCLK1, 0)

    board.digital_write(pinRCLK1, 1)
    board.digital_write(pinRCLK1, 0)
    
    # pins should be written g - a
    # connect the shift reg to the 7 seg accordingly
    for i in range(6, -1, -1): # write value to the 7 seg
        board.digital_write(pinSER1, segments[i])
        board.digital_write(pinSRCLK1, 1)
        board.digital_write(pinSRCLK1, 0)
   
    board.digital_write(pinRCLK1, 1)
    board.digital_write(pinRCLK1, 0)
    
    board.digital_write(digitPins[digit - 1], 0) # turn on the digit pin
    time.sleep(5)

display_character("5", 2)
board.shutdown()
sys.exit(0)
"""

"""
''' VERY VERY VERY IMPORTANT: CONNECT PINS AS GIVEN IN https://docs.arduino.cc/tutorials/communication/guide-to-shift-out '''

pinSER2 = 8
pinSRCLK2 = 9
pinRCLK2 = 10
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

board = pymata4.Pymata4()
board.set_pin_mode_digital_output(pinSER2)
board.set_pin_mode_digital_output(pinSRCLK2)
board.set_pin_mode_digital_output(pinRCLK2)
board.set_pin_mode_digital_output(7)

def display_temeprature(temp):
    # pin mode set during system initialization
    if temp < 18:
        code = TEMP_MAP[0]
    elif 18 <= temp < 20:
        code = TEMP_MAP[1]
    elif 20 <= temp < 22:
        code = TEMP_MAP[2]
    elif 22 <= temp < 24:
        code = TEMP_MAP[3]
    elif 24 <= temp < 26:
        code = TEMP_MAP[4]
    elif 26 <= temp < 28:
        code = TEMP_MAP[5]
    elif 28 <= temp < 30:
        code = TEMP_MAP[6]
    else:
        code = TEMP_MAP[7]

    for _ in range(8):
        board.digital_write(pinSER2, 0)
        board.digital_write(pinSRCLK2, 1)
        board.digital_write(pinSRCLK2, 0)

    board.digital_write(pinRCLK2, 1)
    board.digital_write(pinRCLK2, 0)
    
    for i in range(8):
        board.digital_write(pinSER2, code[i])
        board.digital_write(pinSRCLK2, 1)
        board.digital_write(pinSRCLK2, 0)

    board.digital_write(pinRCLK2, 1)
    board.digital_write(pinRCLK2, 0)

    time.sleep(5)

display_temeprature(20)
board.shutdown()
sys.exit(0)
"""

"""
''' https://docs.arduino.cc/built-in-examples/digital/Button '''

mode = 1
pushButtonPin = 7
redPin = 8
bluePin = 9

board = pymata4.Pymata4()
board.set_pin_mode_digital_input(pushButtonPin)
board.set_pin_mode_digital_output(redPin)
board.set_pin_mode_digital_output(bluePin)

def is_switch_mode(): # ideally the push button press should generate an interrupt, but we do not use async calls in the scope of the unit
    print("Reading push button input...")
    # pin mode set during system initialization
    readings = []
    for _ in range(10):
        readings.append(board.digital_read(pushButtonPin)[0])

    if sum(readings)/ len(readings) >= 0.5: # switch the mode if button pressed
        print(f"{readings}")
        return True
    return False

for i in range(100):
    print(f"i = {i}")
    time.sleep(2)
    if (is_switch_mode() and mode): # if push button pressed, switch current mode
        mode = mode * (-1)
        if mode == 1:
            board.digital_write(bluePin, 0)
            board.digital_write(redPin, 1)
            time.sleep(2)
            
        else:
            board.digital_write(redPin, 0)
            board.digital_write(bluePin, 1)
            time.sleep(2)

board.shutdown()
sys.exit(0)            
"""