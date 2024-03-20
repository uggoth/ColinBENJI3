module_name = 'test_18_SBUS_A_v01.py'
module_description = 'Basic SBUS functionality'
print (module_name, 'starting')

import SBUSReceiver_V06 as SBUSReceiver
import machine
import utime
tx_pin_no = 0
rx_pin_no = 1
uart_no = 0
baud_rate = 100000
uart = machine.UART(uart_no, baud_rate, tx = machine.Pin(tx_pin_no), rx = machine.Pin(rx_pin_no), bits=8, parity=0, stop=2)
my_sbus = SBUSReceiver.SBUSReceiver(uart)

interval = 100

for i in range(5000):
    utime.sleep_us(300)
    my_sbus.get_new_data()
    if i%interval == 0:
        joysticks = my_sbus.get_rx_channels()[0:9]
        if joysticks[0] < 150:
            continue
        print ('loop {:05}'.format(i+1),joysticks)

print (module_name, 'finished')
