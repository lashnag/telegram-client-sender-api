FROM python:3.10-slim

RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-rus

WORKDIR /sender_api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /sender_api

CMD ["sh", "-c", "cd app; uvicorn main_v2:server --host 0.0.0.0 --port 4322 --workers 4 & python main_v1.py"]