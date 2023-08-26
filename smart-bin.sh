echo “shell script”

cd "/home/pi/Documents/new-smartbin-api"
source "venv/bin/activate"
python3 check-running/check_app_running.py
