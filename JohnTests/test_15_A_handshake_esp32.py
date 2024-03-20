#  Test command stream handshake
#  Run in conjunction with HandshakeTestA on the ESP32

module_name = 'test_15_A_handshake_esp32.py'
print (module_name, 'starting')

import time
start_time = time.time()

import pigpio
import serial, sys, select

test_port = serial.Serial(possible_port,timeout=0.1,write_timeout=0.1,baudrate=115200)
time.sleep(5)

handshake_pin = 18
gpio = pigpio.pi()
gpio.set_pull_up_down(handshake_pin, pigpio.PUD_UP)
previous = gpio.read(handshake_pin)
for i in range(9000):
    new = gpio.read(handshake_pin)
    if new != previous:
        print (new)
        previous = new
    time.sleep(0.002)

gpio.stop()
print (module_name, 'finished')
