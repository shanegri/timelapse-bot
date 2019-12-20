#!/usr/bin/python
from Servo import Servo
from Stepper import Stepper
import time, argparse
from datetime import datetime, timedelta
import logging

def main ():
    parser = argparse.ArgumentParser(description="Control hyperlapse")
    parser.add_argument('-t', '--test', dest='test', help='Test mode', action='store_true')
    parser.add_argument('-pt', '--pan_tilt', dest='pan_tilt', help='Set pan & tilt', nargs=2, type=int)
    parser.add_argument('-s', '--start', dest='start', help='Start hyperlapse', nargs=8, type=int)
    args = parser.parse_args()

    servo_pan = Servo(12)
    servo_tilt = Servo(21)
    stepper_left = Stepper([4,17,27,22])
    stepper_right = Stepper([6,13,19,26])

    if args.start:
        logging.basicConfig(level=logging.INFO, filename='/home/pi/hyperlapse/app/api/log', filemode='w', format='%(message)s')

        start_pan = args.start[0] * 10
        start_tilt = args.start[1] * 10
        end_pan = args.start[2] * 10
        end_tilt = args.start[3] * 10
        length = args.start[4] * 1.0
        distance = args.start[5] 
        direction = args.start[6] / 90.0

        reverse = args.start[7] == 1

        velocity = distance / length
        r_velocity = velocity
        l_velocity = velocity

        if direction < 0:
            l_velocity = l_velocity * (1 - abs(direction))

        if direction > 0:
            r_velocity = r_velocity * (1- abs(direction))
                      
        stepper_left.start(l_velocity, reverse)
        stepper_right.start(r_velocity, reverse)
        
        diff_pan = abs(end_pan - start_pan)
        diff_tilt = abs(end_tilt - start_tilt)
        count = max(int(length), max(diff_pan, diff_tilt))

        def expand(list, target):
            retVal = []
            for i in range(len(list)):
                count = target / len(list)
                if target % len(list) - 1 >= i: count += 1
                while count != 0:
                    retVal.append(list[i])
                    count -= 1
            return retVal

        def gen_list(start, end, target):
            if start == end:
                retVal = [start for i in range(target)]
            else:
                inc = 1 if start < end else -1
                retVal = [a for a in range(start, end, inc)]
            if len(retVal) < target:
                retVal = expand(retVal, target)
            return retVal

        pan_list = gen_list(start_pan, end_pan, count)
        tilt_list = gen_list(start_tilt, start_tilt, count)

        wait_time = length / count

        now = datetime.now()
        remaining = count
        logging.info(str(timedelta(seconds=int(wait_time * remaining))) + "s remaining")
        start_time = datetime.now()
        for pan, tilt in zip(pan_list, tilt_list):
            servo_tilt.set_angle(tilt/10.0)
            servo_pan.set_angle(pan/10.0)

            time.sleep(max(0, wait_time - (datetime.now() - start_time).total_seconds()))
            start_time = datetime.now()
            remaining -= 1
            logging.info(str(timedelta(seconds=int(wait_time * remaining))) + "s remaining")

        print datetime.now() - now

        stepper_left.stop()
        stepper_right.stop()

        logging.info("Completed in: " + str(datetime.now() - now))
        while True: continue

        return

    if args.test:
        stepper_left.start(2)
        stepper_right.start(4.3)    
        while True:
            inc = 1
            # for a in range(-45, 45, inc) + range(45,-45,-inc):
            #     servo_tilt.set_angle(a)
            #     time.sleep(.4)
            #     servo_pan.set_angle(a)
            #     time.sleep(.4)
        return

    if args.pan_tilt:
        servo_tilt.set_angle(args.pan_tilt[1])
        servo_pan.set_angle(args.pan_tilt[0])
        return

    if args.hyperlapse:
        inc = 1
        for a in range(-45, 45, inc) + range(45,-45,-inc):
            servo_tilt.set_angle(a)
            time.sleep(.4)
            servo_pan.set_angle(a)
            time.sleep(.4)
        return


if __name__ == "__main__": main()
