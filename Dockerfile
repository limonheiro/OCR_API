#reference: https://github.com/ricktorzynski/ocr-tesseract-docker/blob/master/Dockerfile
FROM ubuntu:22.04 as base
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update &&\
    #tesseract-ocr-por: portuguese
    apt-get install -y tesseract-ocr-por &&\
    apt-get install -y git ffmpeg libsm6 libxext6 python3 python3-pip python3-distutils &&\
    rm -rf /var/lib/apt/lists/* 

FROM base as app
WORKDIR /app
COPY ./app/ /app
RUN pip3 install --no-cache-dir pytesseract opencv-python pillow