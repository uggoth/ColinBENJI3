module_name = 'test_17_PIO_A_allocation_v01.py'

import ColObjects_V16 as ColObjects

print ('allocating')
state_machine_fred = ColObjects.PIO('Fred',0)
print (state_machine_fred)
state_machine_bill = ColObjects.PIO('Bill',0)
print (state_machine_bill)
print (ColObjects.PIO.str_allocated())
print('deallocating')
state_machine_fred.close()
print (ColObjects.PIO.str_allocated())
print('reallocating')
state_machine_john = ColObjects.PIO('John',0)
print (ColObjects.PIO.str_allocated())
