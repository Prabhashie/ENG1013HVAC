import shared
import time
import sys

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
shared.pushButtonPin = 7
shared.redPin = 8
shared.bluePin = 9

shared.set_digital_input_pin_mode([shared.pushButtonPin])
shared.set_digital_output_pin_mode([shared.redPin, shared.bluePin])

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
            shared.board.digital_write(shared.bluePin, 0)
            shared.board.digital_write(shared.redPin, 1)
            time.sleep(2)
            
        else:
            shared.board.digital_write(shared.redPin, 0)
            shared.board.digital_write(shared.bluePin, 1)
            time.sleep(2)

shared.board.shutdown()
sys.exit(0)
"""