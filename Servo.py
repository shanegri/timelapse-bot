# import RPi.GPIO as GPIO
import time
import pigpio


class Servo:

    def __init__(self, pin):
        # GPIO.setmode(GPIO.BOARD)
        self.pi = pigpio.pi()

        self.pin = pin
        self.pi.set_servo_pulsewidth(self.pin, 0)    # off

        # GPIO.setup(self.pin, GPIO.OUT)
        # self.pwm = GPIO.PWM(pin, 50)
        # self.pwm.start(2.5)
    
    # -90 -> 90
    def set_angle(self, angle):
        angle += 90
        angle /= float(180)
        duty = (1 - angle)*2000 + 500
        # self.servo.set_servo(self.pin, duty * 1000)
        # self.pwm.ChangeDutyCycle(duty)
        self.pi.set_servo_pulsewidth(self.pin, duty)    # off
        



if __name__ == "__main__":
    s = Servo(12)

    while True:
        for i in range(-90, 90, 5):
            s.set_angle(i)
            time.sleep(1)


