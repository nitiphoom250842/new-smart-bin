echo “shell script”

cd "/home/pi/Documents/new-smartbin-api"
source "venv/bin/activate"
uvicorn main:app --host 0.0.0.0 --port 80 --env-file .env.prod --reload
