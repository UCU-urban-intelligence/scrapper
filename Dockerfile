FROM python:3.6-alpine

COPY . /scrapper
WORKDIR /scrapper

RUN pip install -r requirements.txt

EXPOSE 8000
