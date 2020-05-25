FROM python:3.7-alpine

WORKDIR /workspace
COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

STOPSIGNAL SIGINT

ENTRYPOINT [ "python", "-u" ]
CMD "api_dig.py"