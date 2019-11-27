import RPi.GPIO as GPIO
import time

class Servo:

    def __init__(self, pin):
        GPIO.setmode(GPIO.BOARD)
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(2.5)
    
    # -90 -> 90
    def set_angle(self, angle):
        angle += 90
        angle /= float(180)
        duty = (1 - angle)*10 + 2.5
        self.pwm.ChangeDutyCycle(duty)

    def release():
        self.pwm.stop()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

    def __del__(self):
        self.release()

if __name__ == "__main__":
    try:
        servo = Servo(32)
        for a in range(-90, 90, 5):
            servo.set_angle(a)
            time.sleep(1)
        while True: continue
    except KeyboardInterrupt:
        GPIO.cleanup()
