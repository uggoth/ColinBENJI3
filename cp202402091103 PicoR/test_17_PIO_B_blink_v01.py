module_name = 'test_17_PIO_B_blink_v01.py'

#################################################################
### NOTE: Needs an LED on GPIO17. (Onboard LED does not work) ###
#################################################################

import time
import rp2
from machine import Pin

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()
    set(pins, 1)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    set(pins, 0)   [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    wrap()

red_pin_no = 25
red_sm = rp2.StateMachine(0, blink, freq=2000, set_base=Pin(red_pin_no))
red_sm.active(1)
time.sleep(4)

#blue_pin_no = 22
#blue_sm = rp2.StateMachine(1, blink, freq=2000, set_base=Pin(blue_pin_no))
#blue_sm.active(1)
#time.sleep(1)

#green_pin_no = 18
#green_sm = rp2.StateMachine(3, blink, freq=2000, set_base=Pin(green_pin_no))
#green_sm.active(1)
#time.sleep(1)

red_sm.active(0)
#blue_sm.active(0)
#green_sm.active(0)

red = Pin(red_pin_no,Pin.OUT)
red.value(0)
#blue = Pin(blue_pin_no,Pin.OUT)
#blue.value(0)
#green = Pin(green_pin_no,Pin.OUT)
#green.value(0)
