# core\light.py

class Light:
    def __init__(self, status_light:bool,status_test:bool):
        self.status_light = status_light
        self.status_test = status_test
        
    def setLight(self):
        data ={"status":200,"message":None}
        if(self.status_test):
            if(self.status_light):
                data['message']='for test open light done'
            else:
                data['message']='for test close light done'
        else:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)

            lightPIN = 13
            if(self.status_test):
                if(self.status_light):
                    GPIO.output(lightPIN, True)
                    data['message']='open light done'
                else:
                    GPIO.output(lightPIN, False)
                    data['message']='open light close'

        return data
    
    