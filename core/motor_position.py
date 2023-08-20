# core\motor_position.py
class MotorPosition:
    def __init__(self,class_name_prediction:object,status_test:bool):
        self.class_name_prediction = class_name_prediction
        self.status_test = status_test
        
        
    def setMoter(self):
        print("MotorPosition ",self.class_name_prediction,self.status_test)

        return 