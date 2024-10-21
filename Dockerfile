FROM python:3.10-slim

RUN apt install python3-pip
RUN pip install pytest requests
RUN mkdir /home/python/test
COPY . /home/python/test
WORKDIR /home/python/test