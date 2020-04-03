FROM python:3.7.7-alpine3.11

ADD . /app
WORKDIR /app

EXPOSE 5000

RUN pip3 install -r requirements.txt

CMD python3 -u app.py
