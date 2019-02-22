FROM python:3.6

ENV LANG C.UTF-8
RUN mkdir /app
WORKDIR /app
ADD requirements/ /app/requirements/
RUN pip install -r /app/requirements/test.txt
ADD . /app
WORKDIR /app