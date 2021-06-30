FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update --fix-missing && apt-get upgrade -y \
	&& apt-get autoremove \
	&& apt-get autoclean
RUN apt-get install -y apt-utils ffmpeg python3.6.2 python3-pip git nano

ARG PROJECT=mytts
ARG PROJECT_DIR=/${PROJECT}
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN git clone https://github.com/nsu-ai/russian_g2p \
	&& cd russian_g2p \
	&& pip3 install . \
	&& cd .. && rm -rf russian_g2p

RUN apt-get install -y locales && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

CMD python3 daemon_clean_wav.py start \
	& gunicorn --access-logfile - -w 2 --threads 30 --bind 0.0.0.0:5000 controller:app --timeout 15000
