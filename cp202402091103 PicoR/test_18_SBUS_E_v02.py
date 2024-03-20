module_name = 'test_18_SBUS_E_v02.py'
description = 'testing and calibrating SBUS objects'
import ThisPico_R_V38 as ThisPico
ColObjects = ThisPico.ColObjects
import utime

my_sbus = ThisPico.ThisSbusReceiver()
print (my_sbus)
my_fore_and_aft = my_sbus.fore_and_aft
my_spin = my_sbus.spin
my_switch = my_sbus.switch
my_knob = my_sbus.knob
bad_gets = 0
good_gets = 0

print ("Loop F&A  Spn  Swi  Kno")
for i in range(20):
    utime.sleep(0.5)
    fore_and_aft_value = my_fore_and_aft.get()
    if fore_and_aft_value is None:
        bad_gets += 1
        continue
    else:
        good_gets += 1
        spin_value = my_spin.get()
        switch_value = my_switch.get()
        knob_value = my_knob.get()
        print ("{:3.0f}  {:3.0f}  {:3.0f}  {:3.0f}  {:3.0f}".format(i+1, fore_and_aft_value, spin_value, switch_value, knob_value))

print (bad_gets,'bad gets    ',good_gets,'good gets')

my_sbus.close()

print ('--- AFTER CLOSE --')
print (ColObjects.ColObj.str_allocated())
print (module_name, 'finished')
