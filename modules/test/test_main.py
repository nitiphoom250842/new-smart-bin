from .core.core_test import CoseTests

class Tests:
    def __init__(self, status_light):
        self.status_light = status_light
        
    def setTest(self):
        print("Hello my test ",self)
