FROM ubuntu:16.04

RUN \
 apt-get update \
 && apt-get install -y software-properties-common python-software-properties apt-transport-https \
 && add-apt-repository ppa:ubuntugis/ppa \
 && add-apt-repository ppa:deadsnakes/ppa \
 && apt-get update \
 && apt-get install -y build-essential python3.6 python3.6-dev curl

COPY . /scrapper
WORKDIR /scrapper

RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6
RUN python3.6 -m pip install -r requirements.txt

EXPOSE 8000
