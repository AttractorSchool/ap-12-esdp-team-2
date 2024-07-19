FROM python:3.11-alpine

RUN apk add --no-cache netcat-openbsd postgresql-client

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r /tmp/requirements.txt

#================================================
# Code
#================================================
COPY . /proj
WORKDIR /proj
