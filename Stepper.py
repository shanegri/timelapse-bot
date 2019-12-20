# import RPi.GPIO as GPIO
import time
import threading
import pigpio
from datetime import datetime 

class Stepper:

    steps = [
        [1,0,0,0],
        # [1,1,0,0],
        [0,1,0,0],
        # [0,1,1,0],
        [0,0,1,0],
        # [0,0,1,1],
        [0,0,0,1],
        # [1,0,0,1]
    ]

    def __init__(self, pins):
        self.pi = pigpio.pi()
        # GPIO.setmode(GPIO.BOARD)
        self.pins = pins
        self.speed = 0.001
        self.running = False
        for pin in self.pins:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            # GPIO.setup(pin, GPIO.OUT)
            # GPIO.output(pin, 0)
    
    def set_rpm():
        return

    def step(self):
        step_dist = 134.0 / 2048.0
        step_wait = step_dist / self.velocity
        # count = 0
        # now = datetime.now()
        step_order = [3,2,1,0] if self.reverse else range(4)
        while self and self.running:
            for step in step_order:
                start_step_time = datetime.now()
                for pin in range(4):
                    self.pi.write(self.pins[pin], self.steps[step][pin])

                # count += 1
                # if count >= 2048: 
                #     print (datetime.now() - now).total_seconds()
                #     return

                step_diff = (datetime.now() - start_step_time).total_seconds()

                time.sleep(max(step_wait - step_diff, 0))    

    def start(self, velocity, reverse):
        self.velocity = velocity
        self.reverse = reverse
        self.t = threading.Thread(target=self.step)
        self.t.setDaemon(True)
        self.running = True
        self.t.start()

    def stop(self):
        self.running = False
        self.t.join()

    # def __del__(self):
    #     self.stop()



if __name__ == "__main__":
    try:
        stepper_left = Stepper([6,13,19,26])
        # stepper_right = Stepper([7,11,13,15])
        # stepper_left.start()
        stepper_left.start()
        while True: continue
    except KeyboardInterrupt:
        pass
        # stepper_left.stop()
        # stepper_right.stop()
        # GPIO.cleanup()
