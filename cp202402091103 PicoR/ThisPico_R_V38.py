module_name = 'ThisPico_R_V38.py'

if __name__ == "__main__":
    print (module_name, 'starting\n')

import GPIOPico_V30 as GPIO
ColObjects = GPIO.ColObjects
import Motor_V07 as Motor
import NeoPixel_V16 as NeoPixel
import SBUSReceiver_V06 as SBUSReceiver
import CommandStreamPico_V06 as CommandStream
import utime
import machine
import _thread

class ThisPico():
    opened = {}
    def add(this_object):
        ThisPico.opened[this_object.name] = this_object  
    def remove(this_object):
        del ThisPico.opened[this_object.name]  
    def str_opened():
        output = ''
        for this_name in sorted(ThisPico.opened):
            output += this_name + '\n'
        return output
    def close_all():
        for this_name in ThisPico.opened:
            ThisPico.opened[this_name].close()
    def __init__(self):
        self.name = 'PICOR'
        self.description = 'Pico R. No WiFi'

class ThisVSYS(GPIO.Volts):
    def __init__(self):
        super().__init__('VSYS',29)
        ThisPico.add(self)
    def close(self):
        ThisPico.remove(self)
        super().close()


class ThisOnboardLED(ColObjects.ColObj):
    def __init__(self):
        super().__init__('Onboard LED','LED')
        self.led = machine.Pin('LED', machine.Pin.OUT)
        self.is_on = False
    def on(self):
        self.led.on()
        self.is_on = True
    def off(self):
        self.led.off()
        self.is_on = False
    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()

################ Use  Test_08_FIT0441_A  to get pin numbers

class ThisLeftFront(Motor.FIT0441BasicMotor):
    def __init__(self):
        speed_pin_no     = 10    # blue
        pulse_pin_no     = 11  # green
        direction_pin_no = 12  # yellow
        super().__init__('Left Front', direction_pin_no, speed_pin_no)

class ThisLeftBack(Motor.FIT0441BasicMotor):
    def __init__(self):
        speed_pin_no     = 6
        pulse_pin_no     = 7
        direction_pin_no = 8
        super().__init__('Left Back', direction_pin_no, speed_pin_no)
       
class ThisRightFront(Motor.FIT0441BasicMotor):
    def __init__(self):
        speed_pin_no     = 21     # blue
        pulse_pin_no     = 20    # green
        direction_pin_no = 19    # yellow
        super().__init__('Right Front', direction_pin_no, speed_pin_no)

class ThisRightBack(Motor.FIT0441BasicMotor):
    def __init__(self):
        speed_pin_no     = 2
        pulse_pin_no     = 3
        direction_pin_no = 4
        super().__init__('Right Back', direction_pin_no, speed_pin_no)

class ThisDriveTrainWithHeadlights(ColObjects.ColObj):
    def __init__(self):
        super().__init__('Pico R Drive Train')
        self.headlight = ThisHeadlight()
        self.headlight.fill_sector('front_right_centre','white')
        self.headlight.fill_sector('front_left_centre','white')
        self.headlights_enabled = True
        self.motor_rf = ThisRightFront()
        self.motor_rb = ThisRightBack()
        self.motor_lf = ThisLeftFront()
        self.motor_lb = ThisLeftBack()
        self.mixer = Motor.Mixer('Pico R Mixer')
    def stop(self):
        self.motor_lf.stop()
        self.motor_rf.stop()
        self.motor_lb.stop()
        self.motor_rb.stop()
    def drive(self, spin, fore_and_aft, crab):
        lf_level, rf_level, lb_level, rb_level = self.mixer.mix(spin, fore_and_aft, crab)
        self.motor_lf.run(-lf_level)
        self.motor_rf.run(rf_level)
        self.motor_lb.run(-lb_level)
        self.motor_rb.run(rb_level)
        if self.headlights_enabled:
            if sum([lf_level, lb_level]) > sum([rf_level, rb_level]):
                self.headlight.spr()
            elif sum([lf_level, lb_level]) < sum([rf_level, rb_level]):
                self.headlight.spl()
            elif sum([lf_level, rf_level, lb_level, rb_level]) >= 0:
                self.headlight.fwd()
            else:
                self.headlight.rev()
        else:
            self.headlight.off()
            return
    def close(self):
        self.headlight.close()
        self.motor_rf.close()
        self.motor_rb.close()
        self.motor_lf.close()
        self.motor_lb.close()
        super().close()

class ThisSbusReceiver(ColObjects.ColObj):
    def __init__(self):
        super().__init__('FrSKY')
        self.tx_pin_no = 0
        self.rx_pin_no = 1
        self.uart_no = 0
        self.baud_rate = 100000
        self.uart = machine.UART(self.uart_no, self.baud_rate, tx = machine.Pin(self.tx_pin_no), rx = machine.Pin(self.rx_pin_no), bits=8, parity=0, stop=2)
        self.sbus = SBUSReceiver.SBUSReceiver(self.uart)
        self.thread_enable = True
        self.thread_running = False
        self.joystick_raws = [0,0,0,0,0,0]
        self.fore_and_aft_interpolator = ColObjects.Interpolator('fore_and_aft Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        self.spin_interpolator = ColObjects.Interpolator('spin Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        self.switch_interpolator = ColObjects.Interpolator('Switch 4 Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
        self.knob_interpolator = ColObjects.Interpolator('Knob 5 Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        self.fore_and_aft = ColObjects.Joystick('fore_and_aft', self, 2, self.fore_and_aft_interpolator)
        self.spin = ColObjects.Joystick('spin', self, 1, self.spin_interpolator)
        self.switch = ColObjects.Joystick('Switch', self, 4, self.switch_interpolator)
        self.knob = ColObjects.Joystick('Knob', self, 5, self.knob_interpolator)
        self.my_thread = _thread.start_new_thread(self.thread_code, ())

    def __str__(self):
        outstring = self.name + '\n'
        return outstring

    def thread_code(self):
        self.thread_running = True
        while True:
            if not self.thread_enable:
                break
            utime.sleep_us(300)
            self.sbus.get_new_data()
            self.joystick_raws = self.sbus.get_rx_channels()[0:6]
        self.thread_running = False

    def get(self):
        max_attempts = 15
        for i in range(max_attempts):
            utime.sleep_us(400)
            spin_raw = self.joystick_raws[1]
            if spin_raw > 15:
                break
        if i == max_attempts:
            return None
        return self.joystick_raws
        
    def close(self):
        self.fore_and_aft.close()
        self.spin.close()
        self.switch.close()
        self.knob.close()
        self.fore_and_aft_interpolator.close()
        self.spin_interpolator.close()
        self.switch_interpolator.close()
        self.knob_interpolator.close()
        self.thread_enable = False
        utime.sleep_ms(100)
        if self.thread_running:
            print ('error thread not closed')
        super().close()

class ThisHeadlight(NeoPixel.NeoPixel):
    def __init__(self):
        super().__init__(name='Headlights', pin_no=18, no_pixels=14, mode='GRB')
        self.sectors['front_right_centre'] = [0,0]
        self.sectors['front_right_rim'] = [1,6]
        self.sectors['front_left_centre'] = [7,7]
        self.sectors['front_left_rim'] = [8,13]
    def fwd(self):
        self.fill_sector('front_right_centre','white')
        self.fill_sector('front_left_centre','white')
        self.fill_sector('front_right_rim','white')
        self.fill_sector('front_left_rim','white')
        self.show()
    def rev(self):
        self.fill_sector('front_right_centre','white')
        self.fill_sector('front_left_centre','white')
        self.fill_sector('front_right_rim','red')
        self.fill_sector('front_left_rim','red')
        self.show()
    def spl(self):
        self.fill_sector('front_right_centre','white')
        self.fill_sector('front_left_centre','red')
        self.fill_sector('front_right_rim','white')
        self.fill_sector('front_left_rim','red')
        self.show()
    def spr(self):
        self.fill_sector('front_right_centre','red')
        self.fill_sector('front_left_centre','white')
        self.fill_sector('front_right_rim','red')
        self.fill_sector('front_left_rim','white')
        self.show()        

class ThisRearLight(NeoPixel.NeoPixel):
    def __init__(self):
        super().__init__(name='Rear Light', pin_no=15, no_pixels=7, mode='GRBW')
        self.sectors['rear_light_centre'] = [0,0]
        self.sectors['rear_light_rim'] = [1,6]

class ThisRLIR(GPIO.IRSensor):
    def __init__(self):
        super().__init__('Rear Left Infra-Red',17)

class ThisRRIR(GPIO.IRSensor):
    def __init__(self):
        super().__init__('Rear Right Infra-Red',16)

class TheseIRSensors():
    def __init__(self):
        self.rlir = ThisRLIR()
        self.rrir = ThisRRIR()
        self.ir_list = [self.rlir, self.rrir]

class ThisDIP_1(GPIO.Switch):
    def __init__(self):
        super().__init__('DIP_1', 14)

class ThisHandshake(GPIO.DigitalOutput):
    def __init__(self):
        super().__init__('Pi Handshake','OUTPUT',9)

class ThisCommandStream(CommandStream.CommandStream):
    def __init__(self):
        self.handshake = ThisHandshake()
        super().__init__('From Pi', self.handshake)

if __name__ == "__main__":
    print (module_name, 'finished')
