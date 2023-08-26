import time
from .ultrasonic import Ultrasonic
import os

if os.getenv("ENV") == "prod":
    import RPi.GPIO as GPIO


class Door:
    def __init__(self):
        pass

    def open(self):
        servoPOW = 6
        servoPIN = 26
        lightPIN = 13

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)
        GPIO.setup(servoPOW, GPIO.OUT)
        GPIO.setup(lightPIN, GPIO.OUT)

        GPIO.output(servoPOW, True)
        p = GPIO.PWM(servoPIN, 50)
        p.start(6.9)
        p.ChangeDutyCycle(3.5)
        time.sleep(1)
        p.stop(self)

    def close():
        servoPOW = 6
        servoPIN = 26
        lightPIN = 13

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)
        GPIO.setup(servoPOW, GPIO.OUT)
        GPIO.setup(lightPIN, GPIO.OUT)

        p = GPIO.PWM(servoPIN, 50)
        p.start(3.5)
        p.ChangeDutyCycle(6.9)
        time.sleep(1)
        p.stop()
        GPIO.output(servoPOW, False)

    def setDoor(self):
        self.open()
        process_detect_trash = Ultrasonic()
        data_detact = process_detect_trash.isHaveObject()
        self.close()

        if data_detact == 1:
            return True
        else:
            return False
