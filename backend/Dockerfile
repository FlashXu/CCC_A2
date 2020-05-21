FROM python:3.7-alpine

WORKDIR /code

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

STOPSIGNAL SIGINT

CMD python3 app.py
