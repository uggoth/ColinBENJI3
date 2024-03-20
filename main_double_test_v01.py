module_name = 'main_double_test_v01'
print (module_name, 'starting')
print ('**** Expects  main_test_command_stream_B  to be running on the Pico')
print ('**** Expects  CommandProtocolTestA  to be running on the ESP32')

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

pico_found = False
gpio = pigpio.pi()
pico_handshake = CommandStream.Handshake(4, gpio)
my_pico = CommandStream.Pico(pico_name, gpio, pico_handshake)
if my_pico.name != pico_name:
    print ('**** Expected Pico:', pico_name, 'Got:', my_pico.name,'****')
else:
    print ('Connected to Pico OK')
    print (my_pico)
    pico_found = True

esp32_found = False
expected_esp32 = 'LINES'
esp32_handshake = CommandStream.Handshake(18, gpio)
my_esp32 = CommandStream.Pico(expected_esp32, gpio, esp32_handshake)
if my_esp32.name != expected_esp32:
    print ('**** Expected ESP32:', expected_esp32, 'Got:', my_esp32.name,'****')
else:
    print ('Connected to ESP32 OK')
    print (my_esp32)
    esp32_found = True

number_length = 4
delay = 0.1
serial_no = 0
servo_speed = 90
print_interval = 1000
exiting = False
finished = False

print ('Main Loop')

commands = [['P','WHOU',10],
            ['P','HFWD',1000],
            ['P','HREV',1000],
            ['E','FLA+',1000],
            ['E','FLA-',1000],
            ['P','STOP',10]]

i = 0
for command_set in commands:
    i += 1
    if exiting:
        command = 'EXIT'
        finished = True
    serial_no += 1
    if serial_no > 9999:
        serial_no = 1
    serial_no_string = '{:04.0f}'.format(serial_no)
    which_device = command_set[0]
    command = command_set[1]
    duration = command_set[2]
    try:
        if which_device == 'P':
            if pico_found:
                serial_no_back, feedback, data = my_pico.do_command(serial_no_string, command)
            else:
                print ('Command',command,'ignored. No Pico')
                continue
        elif which_device == 'E':
            if esp32_found:
                serial_no_back, feedback, data = my_esp32.do_command(serial_no_string, command)
            else:
                print ('Command',command,'ignored. No ESP32')
                continue
        else:
            raise (ColObj.ColError('Bad device', which_device))
        if feedback == 'EXIT':
            exiting = True
            continue
        elif feedback == 'OKOK':
            print (command + 'OKOK')
    except Exception as err:
        print ('**** bad interaction ****', err)
        continue
    time.sleep(duration / 1000.0)

my_pico.close()
my_esp32.close()

print (module_name, 'finished')
