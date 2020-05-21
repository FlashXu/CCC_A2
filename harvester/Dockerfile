FROM python:3.7-alpine

WORKDIR /workspace
COPY requirement.txt ./

ENV INDEX -1

RUN pip install --no-cache-dir -r requirement.txt

STOPSIGNAL SIGINT

CMD python -u api_dig.py $INDEX