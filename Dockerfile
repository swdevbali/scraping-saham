FROM python:3.6-stretch

MAINTAINER Ihfazhillah <mihfazhillah@gmail.com>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir serversaham
WORKDIR /serversaham
ADD requirements.txt /serversaham/
RUN pip install -U pip
RUN pip install -r requirements.txt

COPY serversaham/ /serversaham


