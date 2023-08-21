# core\motor_position.py
class MotorPosition:
    def __init__(self,class_name_prediction:object):
        self.class_name_prediction = class_name_prediction

        
        
    def setMoter(self):
        data ={'can':0,'pet':0,'plastic':0,'unknown':0}
        

        import time
        from serial import Serial
        import os
        import json

        port = '/dev/ttyUSB0'
        allport = os.popen('ls /dev/ttyUSB*').read()
        for p in allport.split('\n'):
            if 'ttyUSB_DEVICE1' not in p:
                port = p
                break

        ser = Serial(
                port=port,
                baudrate = 9600,
                timeout = 5
            )

        time.sleep(2)

        # send = str(input("type : ")) + '\n'
        send = f"{self.class_name_prediction['id']}\n"

        ser.write(send.encode())

        while True:
            output = ser.readline().decode().rstrip()

            if output != "":
                output = output.replace("'", '"')
                output = json.loads(output)
                # [update] send data to server 
                # update_bin(output['can'], output['pete'], output['plastic'], output['other'])
                # update_cc(output['can'], output['pete'], output['plastic'], output['other'])
                # print("output :", output)
                data['can']=output['can']
                data['pet']=output['pete']
                data['plastic']=output['plastic']
                data['unknown']=output['other']
                break


        return data