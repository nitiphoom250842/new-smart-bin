import psutil
import os
import datetime
from core.log import LogSystems


def checkIfProcessRunning(processName):
    """
    Check if there is any running process that contains the given name processName.
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        # print('1')
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


while True:
    # checkIfProcessRunning('11461')
    # print(checkIfProcessRunning('run-gui.sh'))
    if checkIfProcessRunning("smart-bin-api.sh") == False:
        os.system("sh smart-bin-api.sh")
        data = LogSystems.write_csv_file(None, "error")
        time_kill = str(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S"))
        with open("/home/pi/Desktop/log_killer.txt", "a") as f:
            f.writelines(time_kill + "/n")
