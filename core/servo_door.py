import time

class Door:

    def __init__(self):
        pass

    def open(self):
        import RPi.GPIO as GPIO
        

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
        import RPi.GPIO as GPIO
        

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
    

    def detect_hand(self):
        self.close()
        pass


    def setDoor(self):
        self.open()
        self.detect_hand()
        
        
        