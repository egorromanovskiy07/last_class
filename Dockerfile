FROM python:3.10-slim

RUN apt update
RUN apt install python3-pip -y
RUN pip install pytest requests
RUN mkdir -p /home/python/test
COPY . /home/python/test
WORKDIR /home/python/test