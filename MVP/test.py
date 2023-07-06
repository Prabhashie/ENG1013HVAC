from shared import *
from pymata4 import pymata4
import time
import math
import sys

# board = pymata4.Pymata4() # arduino board instance
# board.set_pin_mode_digital_output(7)
# board.set_pin_mode_digital_output(8)

# test 1 => 
# keeps the LED on forever, even after the program has finished execution
# turns off when the program is run again
# board.digital_write(7, 1)

# test 2 => 
# keeps the LED on forever, even after the program has finished execution
# turns off when the program is run again
# board.digital_write(7, 1)
# time.sleep(2)

# test 3 => 
# keeps the LED on, stays on for 2s, then turns off
# board.digital_write(7, 1)
# time.sleep(2)
# board.digital_write(7, 0)

# test 4 => 
# keeps the LEDs on forever, even after the program has finished execution
# turns off when the program is run again
# board.digital_write(7, 1)
# board.digital_write(8, 1)

# test 5 => 
# keeps the LEDs on forever, even after the program has finished execution
# turns off when the program is run again
# board.digital_write(7, 1)
# board.digital_write(8, 1)
# time.sleep(2)

# test 6 => 
# keeps the LEDs on, stays on for 2s, then turns off
# board.digital_write(7, 1)
# board.digital_write(8, 1)
# time.sleep(2)
# board.digital_write(7, 0)
# board.digital_write(8, 0)

# test 7 => 
# keeps each LEDs on, stays on for 2s, then turns off
# board.digital_write(7, 1)
# time.sleep(2)
# board.digital_write(7, 0)
# board.digital_write(8, 1)
# time.sleep(2)
# board.digital_write(8, 0)

# test 8 => 
# turns on for a very short time and turns off. Not very distinguishable
# board.digital_write(7, 1)
# board.digital_write(7, 0)