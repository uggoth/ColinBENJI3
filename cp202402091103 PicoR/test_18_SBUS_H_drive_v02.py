module_name = 'test_18_SBUS_H_drive_v02.py'
description = 'testing object with headlights'
import ThisPico_R_V39 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
print (my_sbus)
my_train = ThisPico.ThisDriveTrainWithHeadlights()
print (my_train)

my_fore_and_aft = my_sbus.fore_and_aft
my_spin = my_sbus.spin
my_switch = my_sbus.switch
my_knob = my_sbus.knob
crab_value = 0  #  do not assume mecanum
bad_gets = 0
for i in range(100):
    utime.sleep_us(300)
    fore_and_aft_value = my_fore_and_aft.get()
    spin_value = my_spin.get()
    switch_value = my_switch.get()
    knob_value= my_knob.get()
    if fore_and_aft_value is None:
        bad_gets += 1
        continue
    else:
        print (i, fore_and_aft_value, spin_value)
        my_train.drive(fore_and_aft_value, spin_value, crab_value)
    utime.sleep_ms(100)

print (bad_gets,'bad gets')

#my_train.headlight.off()
my_train.stop()
my_train.close()
my_sbus.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
