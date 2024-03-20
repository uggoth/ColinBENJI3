module_name = 'test_17_PIO_E_read_PWM_v04.py'
print (module_name)

#   Use square wave signal generator set to 1kHz frequency. Duty irrelevant

import utime
import rp2
from machine import Pin

@rp2.asm_pio()
def measure():
    wrap_target()
    wait(0,pin,0)  #  don't start in the middle of a pulse
    wait(1,pin,0)
    mov(x,invert(null))
    label('loop')    
    jmp(x_dec,'pin_on') #  Note: x will never be zero. We just want the decrement
    nop()  
    label('pin_on')
    jmp(pin, 'loop')
    mov(isr,invert(x))
    push(noblock)
    wrap()

sm_hertz = 100000  #  needs to be multiple readings per square wave cycle

sm0_pin = Pin(17, Pin.IN, Pin.PULL_DOWN)  # Pin.PULL_DOWN   Pin.PULL_UP   None

sm0 = rp2.StateMachine(0, measure, freq=sm_hertz, in_base=sm0_pin, jmp_pin=sm0_pin)

for i in range(50):  #  arbitrary test duration
    utime.sleep_ms(100)
    if sm0.rx_fifo():
        y = sm0.get()
        print ('sm',i,y)

sm0.active(0)

print (module_name, 'finished')
