# core\prediction_image.py

from mimetypes import guess_type
import cv2
from fastapi import HTTPException
import requests
import os
import time

from core.custom_exception import APIPredictionError, CameraError, DoorError, MotorError, RemoveImageError
from .motor_position import MotorPosition
from .servo_door import Door


class PredictionImage:
    def __init__(self, accessToken: str, type_point: str, status_test: bool):
        self.accessToken = accessToken
        self.type_point = type_point  # donate, undonate
        self.status_test = status_test

    def create_name(self):
        seconds = time.time()
        img_name = str(seconds).split(".")[0] + ".jpg"

        return img_name

    def cap_image(self):
        try:
            img_name = self.create_name()
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
            cap.set(cv2.CAP_PROP_EXPOSURE, 25)

            cnt = 0
            while cnt < 5:
                ret, frame = cap.read()
                cnt += 1

            # ret, frame = cap.read()

            if ret:
                image_origin = "assets/image/" + "origin-" + img_name.split(".")[0] + ".jpg"
                cv2.imwrite(image_origin, frame)

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                image_grey = "assets/image/" + "grey-" + img_name
                cv2.imwrite(image_grey, gray)
            else:
                image_grey = -1
                image_origin = -1
            """
            
            image_origin = 'assets/image/' + 'origin-' + img_name.split('.')[0] + '.jpg'
            image_grey = 'assets/image/' + 'grey-' + img_name
            os.system('sudo fswebcam -S 20 --no-banner -d /dev/video1 -r 1280x720 ' + image_origin)
            os.system('sudo fswebcam -S 20 --no-banner -d /dev/video1 -r 1280x720 ' + image_grey)
            """
            cap.release()
            cv2.destroyAllWindows()

            return image_grey, image_origin, img_name
        except:
            raise CameraError()

    def prediction_login(self, image_origin):

        url = os.getenv("BASE_URL_API_AI") + "prediction/"
        headers = {
            "X-Bin-ID": os.getenv("X_BIN_ID"),
            "X-Bin-Client": os.getenv("X_BIN_CLIENT"),
            "Authorization": f"Bearer {self.accessToken}",
        }

        image_type = guess_type(image_origin)[0]
        files = {"image": (image_origin, open(image_origin, "rb"), image_type)}
        try:
            return requests.request(
                "POST", url, files=files, headers=headers, verify=False
            )
        except:
            raise APIPredictionError()

    def prediction_donate(self, image_origin):

        url = os.getenv("BASE_URL_API_AI") + "prediction/?mode=donate"
        headers = {
            "X-Bin-ID": os.getenv("X_BIN_ID"),
            "X-Bin-Client": os.getenv("X_BIN_CLIENT"),
        }

        image_type = guess_type(image_origin)[0]
        files = {"image": (image_origin, open(image_origin, "rb"), image_type)}

        try:
            return requests.request(
                "POST", url, files=files, headers=headers, verify=False
            )
        except:
            raise APIPredictionError()

    def for_test(self):
        image_origin = os.path.join("assets", "images", "plastic.jpg")

        if self.type_point == "donate":
            data = self.prediction_donate(image_origin)
            # print(data.json())
        elif self.type_point == "undonate":
            data = self.prediction_login(image_origin)
            # print(data.json())

        return data
    
    def removeImage(self, path: list):
        for p in path:
            try:  os.remove(p)
            except: raise RemoveImageError()


    def predictions(self):
        # print("PredictionImage ",self.accessToken,self.type_point,self.status_test)
        # image_grey, image_origin, image_name = None
        data_bin_details = {"can": 10, "pet": 50, "plastic": 40, "unknown": 90}
        data = None

        if self.status_test:
            data = self.for_test()
            return {"status": 200, "data": data.json(), "bin_details": data_bin_details}
        else:
            try:
                set_servo_door = Door()
                data_door = set_servo_door.setDoor()

                if data_door:
                    image_grey, image_origin, _ = self.cap_image()

                    if self.type_point == "donate":
                        data = self.prediction_donate(image_origin)
                        # print(data.json())

                    elif self.type_point == "undonate":
                        data = self.prediction_login(image_origin)
                        # print(data.json())

                    if data is not None:
                        setup_motor = MotorPosition(class_name_prediction=data.json())
                        data_bin_details = setup_motor.setMoter()

                    self.removeImage([image_origin, image_grey])

                    return {
                        "status": 200,
                        "data": data.json(),
                        "bin_details": data_bin_details,
                    }

            except DoorError:
                raise DoorError()

            except CameraError:
                raise CameraError()

            except APIPredictionError:
                raise APIPredictionError()

            except MotorError:
                raise MotorError()
            
            except RemoveImageError:
                raise RemoveImageError()
            