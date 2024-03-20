module_name = 'test_15_D_command_stream_v02.py'
print (module_name, 'starting')

import ThisPico_R_V37 as ThisPico
import CommandStreamPico_V05 as CommandStream
import utime

my_handshake = ThisPico.ThisHandshake()
my_stream = CommandStream.CommandStream('From Pi', my_handshake)

print ('*** Close Thonny and start sender on Pi ***')

logging = open(module_name + '.txt\n','w')
logging.write(module_name + ' starting\n\n')

for i in range(10000):
    my_stream.ready()
    utime.sleep_ms(1)
    message = my_stream.get()
    if message:
        my_stream.not_ready()
        logging.write('Received: ' + message + '\n')
        serial_no = message[0:4]
        command = message[4:8]
        if command == 'WHOU':
            my_stream.send('0000PICOA')
            logging.write('Command WHOU\n')
        elif command == 'EXIT':
            my_stream.send('0001OKOK')
            logging.write('Command EXIT\n\n')
            break
        else:
            my_stream.send('BADC')
            logging.write('Command not WHOU\n')

if my_handshake is not None:
    my_handshake.close()
my_stream.close()

logging.write(module_name + ' finished\n\n')
logging.close()
