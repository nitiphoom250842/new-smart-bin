import os
import time

if os.getenv("ENV") == "prod":
    import RPi.GPIO as GPIO


class Ultrasonic:
    def __init__(self):
        pass

    def detect_hand(self):
        GPIO.setmode(GPIO.BCM)
        GPIO_TRIGGER = 20
        GPIO_ECHO = 21
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        # 6.46451711655 detect hand

        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        begin_time = time.time()
        
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
            if time.time() - begin_time > 1:
                break

        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return abs(distance)

    def detect_trash(self):
        GPIO.setmode(GPIO.BCM)
        GPIO_TRIGGER = 27
        GPIO_ECHO = 22
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)

        GPIO.output(GPIO_TRIGGER, True)

        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        begin_time = time.time()

        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
            if time.time() - begin_time > 1:
                break

        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        return abs(distance)

    def isHaveObject(self):
        start_time = time.time()

        while True:
            dist = self.detect_hand()
            hand = self.detect_trash()
            time.sleep(1)

            if hand > 15:
                if dist < 23:
                    time.sleep(1)
                    return 1

                if (time.time() - start_time) > 10:
                    return 0
