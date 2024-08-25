export $(cat .env | xargs)
uvicorn main:app --host 127.0.0.1 --port 8888 --reload --log-level debug