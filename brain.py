from Servo import Servo
from Stepper import Stepper
import RPi.GPIO as GPIO
import time

if __name__ == "__main__":
    try:
        servo_pan = Servo(32)

        stepper_left = Stepper([7,11,13,15])
        stepper_right = Stepper([31,33,35,37])

        stepper_left.start()
        stepper_right.start()    

        servo_pan.set_angle(0)
    except KeyboardInterrupt:
        stepper_left.stop()
        stepper_right.stop()
        servo_pan.release()
        GPIO.cleanup()
