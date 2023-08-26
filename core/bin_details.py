# core\bin_details.py
import os
import time
import json


if os.getenv("ENV") == "prod":
    from serial import Serial


class BinDetails:
    def __init__(self, status_test):
        self.status_test = status_test

    def checkBinDetails(self):
        data = {"can": 0, "pet": 0, "plastic": 0, "unknown": 0}
        if self.status_test:
            data["can"] = 10
            data["pet"] = 30
            data["plastic"] = 40
            data["unknown"] = 50
        else:
            port = "/dev/ttyUSB0"
            allport = os.popen("ls /dev/ttyUSB*").read()

            for p in allport.split("\n"):
                if "ttyUSB_DEVICE1" not in p:
                    port = p
                    break

            ser = Serial(port=port, baudrate=9600, timeout=5)

            time.sleep(2)

            # send = str(input("type : ")) + '\n'
            send = f"{-1}\n"

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
                    data["can"] = output["can"]
                    data["pet"] = output["pete"]
                    data["plastic"] = output["plastic"]
                    data["unknown"] = output["other"]
                    break

        return {"status": 200, "data": data}


#  docker run -it -e NGROK_AUTHTOKEN=20M5L5imBa6T8hTusEG9r8Y17kI_2Pa6ft7R8U89qPuyGuX7s ngrok/ngrok http 8080
# ngrok config add-authtoken 20M5L5imBa6T8hTusEG9r8Y17kI_2Pa6ft7R8U89qPuyGuX7s
