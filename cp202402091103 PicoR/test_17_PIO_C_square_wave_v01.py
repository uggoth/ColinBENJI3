module_name = 'test_17_PIO_C_square_wave_v01.py'

#################################################################
### NOTE: Connect oscilloscope to GPIO 16                     ###
#################################################################

import time
import rp2
from machine import Pin

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def square():
    wrap_target()
    set(pins, 1)
    set(pins, 0)
    wrap()

square_wave_frequency = 5000

sm = rp2.StateMachine(0, square, freq=square_wave_frequency*2, set_base=Pin(16))

sm.active(1)
time.sleep(3)
sm.active(0)