module_name = 'test_18_SBUS_F_headlight_v01.py'
description = 'testing and calibrating SBUS objects'
import ThisPico_Q_V32 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
print (my_sbus)
my_throttle = my_sbus.throttle
my_steering = my_sbus.steering
my_switch = my_sbus.switch
my_knob = my_sbus.knob
my_headlight = ThisPico.ThisHeadlight()

for i in range(1000):
    throttle_value = my_throttle.get()
    if throttle_value is None:
        continue
    else:
        steering_value = my_steering.get()
        switch_value = my_switch.get()
        knob_value = my_knob.get()
        if switch_value < 50:
            my_headlight.off()
        else:
            my_headlight.fill_sector('front_right_centre', 'white')
            my_headlight.fill_sector('front_left_centre', 'white')
            if knob_value < -50:
                my_headlight.fill_sector('front_right_rim', 'red')
                my_headlight.fill_sector('front_left_rim', 'red')
            elif knob_value > -50:
                my_headlight.fill_sector('front_right_rim', 'orange')
                my_headlight.fill_sector('front_left_rim', 'orange')
            if knob_value > 50:
                my_headlight.fill_sector('front_right_rim', 'yellow')
                my_headlight.fill_sector('front_left_rim', 'yellow')
    utime.sleep_ms(5)

my_sbus.close()
my_headlight.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
