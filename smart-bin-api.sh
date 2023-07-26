echo “shell script”

cd "/home/pi/Documents/new-smartbin-api"
source "env/bin/activate"
uvicorn main:app --host 0.0.0.0 --port 80 --env-file .env.dev --reload
