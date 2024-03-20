module_name = 'test_18_SBUS_E_v01.py'
description = 'testing and calibrating SBUS objects'
import ThisPico_R_V38 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
print (my_sbus)
my_throttle = my_sbus.throttle
my_steering = my_sbus.steering
my_switch = my_sbus.switch
my_knob = my_sbus.knob

print ("Loop Thr  Str  Swi  Kno")
for i in range(50):
    throttle_value = my_throttle.get()
    if throttle_value is None:
        continue
    else:
        steering_value = my_steering.get()
        switch_value = my_switch.get()
        knob_value = my_knob.get()
        print ("{:3.0f}  {:3.0f}  {:3.0f}  {:3.0f}  {:3.0f}".format(i+1, throttle_value, steering_value, switch_value, knob_value))
    utime.sleep(0.5)

my_sbus.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
