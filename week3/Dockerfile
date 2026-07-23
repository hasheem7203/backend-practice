from python:3.12-slim

workdir /code

copy requirements.txt .
run pip install --no-cache-dir -r requirements.txt

copy app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]