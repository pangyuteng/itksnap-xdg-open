
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -yq && \
    apt-get install -yq \
    less tzdata curl wget vim \
    python3 python3-dev python3-pip \
    itksnap 

ENV TZ="America/Los_Angeles"

RUN python3 -m pip install pip setuptools --upgrade
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

RUN mkdir -p /opt/citksnap
WORKDIR /opt/citksnap
COPY . .
RUN chmod -R 777 /opt/citksnap
