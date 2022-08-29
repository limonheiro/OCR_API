#reference: https://github.com/ricktorzynski/ocr-tesseract-docker/blob/master/Dockerfile
FROM python:3.10-slim as base
ARG DEBIAN_FRONTEND=noninteractive
ARG USERNAME=userocr_api
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt-get update &&\
    #tesseract-ocr-por: portuguese
    apt-get install -y -qq tesseract-ocr-por &&\
    apt-get install -y -qq --no-install-recommends ffmpeg libsm6 libxext6 sudo&&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/* 

    # Create the user
RUN groupadd --gid $USER_GID $USERNAME &&\
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME &&\
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
     apt-get update &&\
     echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME &&\
     chmod 0444 /etc/sudoers.d/$USERNAME &&\
     export PATH=/home/$USERNAME/.local/bin/:$PATH

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME

FROM base as app

WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --no-cache-dir -r req.txt