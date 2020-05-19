# Our base image is official python 3.7 for Debian 10 (Buster)
# https://hub.docker.com/_/python/
FROM python:3.7.7-buster

# Maintainer information
LABEL vendor="PET_PROJECT"
LABEL maintainer="igorbezr"
LABEL version="alpha"

# Make directory for project code 
WORKDIR /usr/src/ixia_rest_wrapper
RUN mkdir src

# Install required Debian packages (mainly openssl for python)
RUN apt update \
    && apt install -y \
    apt-utils \
    telnet \
    python3-openssl

# Copy source code from Developer workstation to image
COPY src/*.py src/

# Copy requirements and install required pip packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy demo script (if needed)
COPY demo.py .

# Setting up timezone properly (or it will be have UTC time)
ENV TZ='Europe/Moscow'

# Setting up stop signal
STOPSIGNAL SIGTERM

# Setting up python interpreter as an entry point
ENTRYPOINT ["python"]
