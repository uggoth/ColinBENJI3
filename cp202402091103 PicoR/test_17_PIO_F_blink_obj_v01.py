module_name = 'test_17_PIO_F_blink_obj_v01.py'

#################################################################
### NOTE: Needs an LED on GPIO17. (Onboard LED does not work) ###
#################################################################

import time
import rp2
from machine import Pin
import GPIOPico_V30 as GPIO
ColObjects = GPIO.ColObjects

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

fred_state_machine = ColObjects.PIO('Fred PIO',0)
john_state_machine = ColObjects.PIO('John PIO',0)
print (john_state_machine)
john_pio_no = john_state_machine.pio_no
john_pin_no = 25
john_pin = GPIO.LED('John LED', john_pin_no)

sm = rp2.StateMachine(john_pio_no, blink, freq=2000, set_base=Pin(john_pin_no))

sm.active(1)
time.sleep(5)
sm.active(0)

led = Pin(john_pin_no,Pin.OUT)
led.value(0)

fred_state_machine.close()
john_state_machine.close()
john_pin.close()