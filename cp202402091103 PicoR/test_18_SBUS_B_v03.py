module_name = 'test_18_SBUS_B_v03.py'
module_description = 'Calibrating joysticks. Part 1'
print (module_name, 'starting')

import sbus_receiver_3 as sbus_receiver
import machine
import utime
import ColObjects_V16 as ColObjects

tx_pin_no = 0
rx_pin_no = 1
uart_no = 0
baud_rate = 100000
uart = machine.UART(uart_no, baud_rate, tx = machine.Pin(tx_pin_no), rx = machine.Pin(rx_pin_no), bits=8, parity=0, stop=2)
my_sbus = sbus_receiver.SBUSReceiver(uart)

throttle_interpolator = ColObjects.Interpolator('Throttle Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
steering_interpolator = ColObjects.Interpolator('Steering Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
switch_interpolator = ColObjects.Interpolator('Switch 4 Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
knob_interpolator = ColObjects.Interpolator('Knob 5 Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
interval = 400

print ('Throttle   Steering   Switch4   Knob5')
for i in range(5000):
    utime.sleep_us(300)
    my_sbus.get_new_data()
    if i%interval == 0:
        joysticks = my_sbus.get_rx_channels()[0:6]
        steering_raw = joysticks[1]
        if steering_raw < 15:
            continue
        throttle_raw = joysticks[2]
        switch_4_raw = joysticks[4]
        knob_5_raw = joysticks[5]
        throttle_value = throttle_interpolator.interpolate(throttle_raw)
        steering_value = steering_interpolator.interpolate(steering_raw)
        switch_4_value = switch_interpolator.interpolate(switch_4_raw)
        knob_5_value = knob_interpolator.interpolate(knob_5_raw)
        print ('{:9.1f}{:9.1f}{:9.1f}{:9.1f}'.format(throttle_value, steering_value, switch_4_value, knob_5_value))

print (module_name, 'finished')