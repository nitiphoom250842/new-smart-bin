# core\prediction_image.py

from mimetypes import guess_type
import cv2
import requests
import os
import time
from .motor_position import MotorPosition
from .servo_door import Door


class PredictionImage:
    def __init__(self,accessToken:str,type_point:str,status_test:bool):
        self.accessToken = accessToken
        self.type_point = type_point
        self.status_test = status_test
        

    def create_name(self):
        seconds = time.time()
        imgname = str(seconds).split('.')[0] + '.jpg'

        return imgname
    
    def cap_image(self):
        imgname = self.create_name()
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        #cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        cap.set(cv2.CAP_PROP_EXPOSURE, 25)
        
        cnt = 0
        while cnt < 5:
            ret, frame = cap.read()
            cnt += 1
        
        
        # ret, frame = cap.read()

        if ret:
            image_origin = 'image/' + 'origin-' + imgname.split('.')[0] + '.jpg'
            cv2.imwrite(image_origin, frame)

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image_grey = 'image/' + 'grey-' + imgname
            cv2.imwrite(image_grey, gray)
        else:
            image_grey = -1
            image_origin = -1
        '''
        
        image_origin = 'image/' + 'origin-' + imgname.split('.')[0] + '.jpg'
        image_grey = 'image/' + 'grey-' + imgname
        os.system('sudo fswebcam -S 20 --no-banner -d /dev/video1 -r 1280x720 ' + image_origin)
        os.system('sudo fswebcam -S 20 --no-banner -d /dev/video1 -r 1280x720 ' + image_grey)
        '''
        cap.release()
        cv2.destroyAllWindows()

        return image_grey, image_origin,imgname
    
    def prediction_login(self,image_origin):
    
        url = os.getenv('BASE_URL_API_AI')+'prediction/'
        headers = {
            'X-Bin-ID': os.getenv('X_BIN_ID'),
            'X-Bin-Client': os.getenv('X_BIN_CLIENT'),
            'Authorization': f'Bearer {self.accessToken}'
        }

        image_type = guess_type(image_origin)[0]
        files = {'image': (image_origin, open(image_origin, 'rb'), image_type)}
        try:
            res = requests.request('POST', url, files=files, headers=headers, verify=False)
        except:
            return 404

        return res

    def prediction_donate(self,image_origin):
    
        url = os.getenv('BASE_URL_API_AI')+'prediction/?mode=donate'
        headers = {
           'X-Bin-ID': os.getenv('X_BIN_ID'),
            'X-Bin-Client': os.getenv('X_BIN_CLIENT'),
        }

        image_type = guess_type(image_origin)[0]
        files = {'image': (image_origin, open(image_origin, 'rb'), image_type)}
        
        try:
            res = requests.request('POST', url, files=files, headers=headers, verify=False)
        except:
            return 404
            
        return res
        
    def predictions(self):
        # print("PredictionImage ",self.accessToken,self.type_point,self.status_test)
       
        if(self.status_test):
            pass
        else:
            set_servo_door =Door()
            set_servo_door.setDoor()
            
            
        image_grey, image_origin, image_name = self.cap_image()
        if self.type_point == 'donate':
            data = self.prediction_donate(image_origin)
            # print(data.json())
        elif self.type_point == 'undonate':
            data = self.prediction_login(image_origin)
            # print(data.json())

        setup_motor =MotorPosition(class_name_prediction=data.json(),status_test=self.status_test)
        setup_motor.setMoter()

        return {'status':200,"data":data.json()}

    
    