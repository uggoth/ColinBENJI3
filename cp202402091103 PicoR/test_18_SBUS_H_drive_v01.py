module_name = 'test_18_SBUS_H_drive_v01.py'
description = 'testing object with headlights'
import ThisPico_R_V34 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
print (my_sbus)
my_train = ThisPico.ThisDriveTrainWithHeadlights()
print (my_train)

my_throttle = my_sbus.throttle
my_steering = my_sbus.steering
my_switch = my_sbus.switch
my_knob = my_sbus.knob

bad_gets = 0
for i in range(200):
    utime.sleep_us(300)
    throttle_value = my_throttle.get()
    steering_value = my_steering.get()
    switch_value = my_switch.get()
    knob_value= my_knob.get()
    if throttle_value is None:
        bad_gets += 1
        continue
    else:
        print (i, throttle_value, steering_value)
        my_train.drive(throttle_value, steering_value)
    utime.sleep_ms(100)

print (bad_gets,'bad gets')

#my_train.headlight.off()
my_train.stop()
my_train.close()
my_sbus.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
