module_name = 'ThisPico_R_V35.py'

if __name__ == "__main__":
    print (module_name, 'starting\n')

import GPIOPico_V30 as GPIO
ColObjects = GPIO.ColObjects
import Motor_V06 as Motor
import NeoPixel_V16 as NeoPixel
import SBUSReceiver_V06 as SBUSReceiver
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
        speed_pin_no     = 21    # blue
        pulse_pin_no     = 20    # green
        direction_pin_no = 19    # yellow
        super().__init__('Left Front', direction_pin_no, speed_pin_no)

class ThisLeftBack(Motor.FIT0441BasicMotor):
    def __init__(self):
        speed_pin_no     = 2
        pulse_pin_no     = 3
        direction_pin_no = 4
        super().__init__('Left Back', direction_pin_no, speed_pin_no)

class ThisLeftSide(Motor.Side):
    def __init__(self):
        self.motor_lf = ThisLeftFront()
        self.motor_lb = ThisLeftBack()
        self.motor_list = [self.motor_lf, self.motor_lb]
        super().__init__('Left Side', 'L', self.motor_list)
    def close(self):
        for motor in self.motor_list:
            motor.close()
        super().close()
        
class ThisRightFront(Motor.FIT0441BasicMotor):
    def __init__(self):
        speed_pin_no     = 10     # blue
        pulse_pin_no     = 11    # green
        direction_pin_no = 12    # yellow
        super().__init__('Right Front', direction_pin_no, speed_pin_no)

class ThisRightBack(Motor.FIT0441BasicMotor):
    def __init__(self):
        speed_pin_no     = 6
        pulse_pin_no     = 7
        direction_pin_no = 8
        super().__init__('Right Back', direction_pin_no, speed_pin_no)

class ThisRightSide(Motor.Side):
    def __init__(self):
        self.motor_rf = ThisRightFront()
        self.motor_rb = ThisRightBack()
        self.motor_list = [self.motor_rf, self.motor_rb]
        super().__init__('Right Side', 'R', self.motor_list)
    def close(self):
        for motor in self.motor_list:
            motor.close()
        super().close()


class ThisDriveTrain(ColObjects.ColObj):
    def __init__(self):
        super().__init__('Pico Q Drive Train')
        self.left_side = ThisLeftSide()
        self.right_side = ThisRightSide()
        self.all_motors = []
        for motor in self.left_side.motor_list:
            self.all_motors.append(motor)
        for motor in self.right_side.motor_list:
            self.all_motors.append(motor)
        self.min_throttle = -100
        self.max_throttle = 100
        self.min_steering = -100
        self.max_steering = 100
        self.mode = 'CAR'
        self.millimetre_factor = 30
        self.degree_factor = 30
        self.pulse_factor = 1
        #self.pulse_motor = ThisLeftSide.motor_lb   #  arbitrary
        
    def constrain(self, n, lowest, highest):
        if n > highest:
            a = highest
        elif n < lowest:
            a = lowest
        else:
            a = n
        return a
        
    def drive(self, throttle, steering):
        if self.mode == 'TANK':
            left = self.constrain (throttle, self.min_throttle, self.max_throttle)
            right = self.constrain (steering, self.min_steering, self.max_steering)
        else:
            left = self.constrain (throttle + steering, self.min_throttle, self.max_throttle)
            right = self.constrain (throttle - steering, self.min_throttle, self.max_throttle)
        self.left_side.drive(left)
        self.right_side.drive(right)

    def convert_millimetres_to_milliseconds(self, millimetres, speed):
        milliseconds = int (float(millimetres) * self.millimetre_factor * (100.0 / float(speed)))
        return milliseconds

    def convert_degrees_to_milliseconds(self, millimetres, speed):
        milliseconds = int (float(millimetres) * self.degree_factor * (100.0 / float(speed)))
        return milliseconds

    def convert_millimetres_to_pulses(self, millimetres):
        return int(millimetres * pulse_factor)

    def fwd(self, speed=50, millimetres=50):
        self.left_side.fwd(speed)
        self.right_side.fwd(speed)
        if millimetres > 0:
            ms = self.convert_millimetres_to_milliseconds(millimetres, speed)
            utime.sleep_ms(ms)
            self.stop()
            return ms
        return 0
    
    def fwd_pulses(self, speed, no_pulses):
        for motor in self.all_motors:
            start = motor.get_pulses()
            motor.pulse_endpoint = start + no_pulses
        for motor in self.all_motors:
            motor.clk()
        
    def rev(self, speed=50, millimetres=50):
        self.left_side.rev(speed)
        self.right_side.rev(speed)
        if millimetres > 0:
            ms = self.convert_millimetres_to_milliseconds(millimetres, speed)
            utime.sleep_ms(ms)
            self.stop()
            return ms
        return 0
    def spl(self, speed=90, degrees=90):
        self.left_side.rev(speed)
        self.right_side.fwd(speed)
        if degrees > 0:
            ms = self.convert_degrees_to_milliseconds(degrees, speed)
            utime.sleep_ms(ms)
            self.stop()
            return ms
        return 0
    def spr(self, speed=90, degrees=90):
        self.left_side.fwd(speed)
        self.right_side.rev(speed)
        if degrees > 0:
            ms = self.convert_degrees_to_milliseconds(degrees, speed)
            utime.sleep_ms(ms)
            self.stop()
            return ms
        return 0
    def stop(self):
        self.left_side.stop()
        self.right_side.stop()
    def close(self):
        self.left_side.close()
        self.right_side.close()
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
        self.throttle_interpolator = ColObjects.Interpolator('Throttle Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        self.steering_interpolator = ColObjects.Interpolator('Steering Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        self.switch_interpolator = ColObjects.Interpolator('Switch 4 Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [100.0, 100.0, 0.0, 0.0, -100.0, -100.0])
        self.knob_interpolator = ColObjects.Interpolator('Knob 5 Interpolator',
                                                [100, 200, 950, 1050, 1750, 1900], [-100.0, -100.0, 0.0, 0.0, 100.0, 100.0])
        self.throttle = ColObjects.Joystick('Throttle', self, 2, self.throttle_interpolator)
        self.steering = ColObjects.Joystick('Steering', self, 1, self.steering_interpolator)
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
            steering_raw = self.joystick_raws[1]
            if steering_raw > 15:
                break
        if i == max_attempts:
            return None
        return self.joystick_raws
        
    def close(self):
        self.throttle.close()
        self.steering.close()
        self.switch.close()
        self.knob.close()
        self.throttle_interpolator.close()
        self.steering_interpolator.close()
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

class ThisDriveTrainWithHeadlights(ThisDriveTrain):
    def __init__(self):
        super().__init__()
        self.headlight = ThisHeadlight()
        self.headlight.fill_sector('front_right_centre','white')
        self.headlight.fill_sector('front_left_centre','white')
        self.headlights_enabled = True
    def drive(self, throttle_value, steering_value):
        super().drive(throttle_value, steering_value)
        if not self.headlights_enabled:
            self.headlight.off()
            return
        if throttle_value > 0:
            self.headlight.fill_sector('front_right_rim','white')
            self.headlight.fill_sector('front_left_rim','white')
            self.headlight.show()
        elif throttle_value < 0:        
            self.headlight.fill_sector('front_right_rim','red')
            self.headlight.fill_sector('front_left_rim','red')
            self.headlight.show()
        else:
            self.headlight.fill_sector('front_right_rim','off')
            self.headlight.fill_sector('front_left_rim','off')
            self.headlight.show()
    def close(self):
        self.headlight.close()
        super().close()

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

if __name__ == "__main__":
    test_dt = ThisDriveTrain()
    test_sbus = ThisSbusReceiver()
    test_headlight = ThisHeadlight()
    utime.sleep(1)
    test_dt.close()
    test_sbus.close()
    test_headlight.close()
    print ('--- AFTER CLOSE --')
    print (ColObjects.ColObj.str_allocated())
    print (module_name, 'finished')
