import time

from core.custom_exception import DoorError
from .ultrasonic import Ultrasonic
import os

servoPOW = 6
servoPIN = 26
lightPIN = 13

if os.getenv("ENV") == "prod":
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    GPIO.setup(servoPOW, GPIO.OUT)
    GPIO.setup(lightPIN, GPIO.OUT)


class Door:
    def __init__(self):
        pass

    def open(self):
        GPIO.output(servoPOW, True)
        p = GPIO.PWM(servoPIN, 50)
        p.start(6.9)
        p.ChangeDutyCycle(3.5)
        time.sleep(1)
        p.stop()

    def close(self):
        p = GPIO.PWM(servoPIN, 50)
        p.start(3.5)
        p.ChangeDutyCycle(6.9)
        time.sleep(1)
        p.stop()
        GPIO.output(servoPOW, False)

    def setDoor(self):
        try:
            self.open()
            process_detect_trash = Ultrasonic()
            data_detact = process_detect_trash.isHaveObject()
            self.close()

            if data_detact == 1:
                return True
            else:
                return False
        except:
            raise DoorError()
