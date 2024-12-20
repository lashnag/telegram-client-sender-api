FROM python:3.10-slim

WORKDIR /sender_api

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /sender_api

CMD ["sh", "-c", "sleep 30 && python app/main_v1.py && python app/main_v2.py"]