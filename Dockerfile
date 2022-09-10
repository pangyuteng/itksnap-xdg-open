FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -yq python3 python3-dev python3-pip 

#RUN pip install PyQt -y

