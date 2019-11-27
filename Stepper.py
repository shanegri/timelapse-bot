import RPi.GPIO as GPIO
import time
import threading


class Stepper:

    steps = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]
    ]

    def __init__(self, pins):
        GPIO.setmode(GPIO.BOARD)
        self.pins = pins
        self.speed = 0.001 
        self.running = False
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
    
    def set_rpm():
        return

    def step(self):
        while self.running:
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(self.pins[pin], self.steps[halfstep][pin])
                time.sleep(self.speed)    
    
    def start(self):
        self.t = threading.Thread(target=self.step)
        self.running = True
        self.t.start()

    def stop(self):
        self.running = False
        self.t.join()
        while self.t.is_alive(): continue
        for pin in self.pins:
            GPIO.setup(pin, GPIO.IN)

    def __del__(self):
        self.stop()



if __name__ == "__main__":
    try:
        stepper_left = Stepper([31,33,35,37])
        stepper_right = Stepper([7,11,13,15])
        stepper_left.start()
        stepper_right.start()
        while True: continue
    except KeyboardInterrupt:
        stepper_left.stop()
        stepper_right.stop()
        # GPIO.cleanup()
