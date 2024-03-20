module_name = 'main_drive_test_v01'
print (module_name, 'starting')

#### Expects  main_rc_with_arm  to be running on the Pico

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()
CommandStream = ThisPi.CommandStream
AX12Servo = ThisPi.AX12Servo
ColObjects = ThisPi.ColObjects
pico_name = data_values['PICO_NAME']
import time
import pigpio

gpio = pigpio.pi()
handshake = CommandStream.Handshake(4, gpio)
#handshake = None
my_pico = CommandStream.Pico(pico_name, gpio, handshake)
if my_pico.name != pico_name:
    print ('**** Expected Pico:', pico_name, 'Got:', my_pico.name,'****')
else:
    print ('Connected to Pico OK')

loops = 100
number_length = 4
delay = 0.1
serial_no = 0
servo_speed = 90
print_interval = 1000
exiting = False
finished = False

print ('Main Loop')

commands = [['WHOU',10],
            ['DRIV003000000000',1000],
            ['DRIV-03000000000',1000],
            ['DRIV003000000000',1000],
            ['STOP',10]]

i = 0
for command_set in commands:
    i += 1
    if my_pico.valid:
        if exiting:
            command = 'EXIT'
            finished = True
        else:
            command = 'SBUS'
        serial_no += 1
        if serial_no > 9999:
            serial_no = 1
        serial_no_string = '{:04.0f}'.format(serial_no)
        command = command_set[0]
        duration = command_set[1]
        try:
            serial_no_back, feedback, data = my_pico.do_command(serial_no_string, command)
            if feedback == 'EXIT':
                exiting = True
                continue
            elif feedback == 'OKOK':
                print (command + 'OK')
        except Exception as err:
            print ('**** bad interaction ****', err)
            continue
        time.sleep(duration / 1000.0)
    else:
        print ('*** No Pico ***')
        break

my_pico.close()

print (module_name, 'finished')
