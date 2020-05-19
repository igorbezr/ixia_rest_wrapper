# Our base image is official python 3.7 for Debian 10 (Buster)
# https://hub.docker.com/_/python/
FROM python:3.7.7-buster

# Maintainer information
LABEL vendor="PET_PROJECT"
LABEL maintainer="igorbezr"
LABEL version="alpha"

# Make directory for project code 
WORKDIR /usr/src/ixia_rest_wrapper

# Copy requirements and install required pip packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Setting up timezone properly (or it will be have UTC time)
ENV TZ='Europe/Moscow'

# Setting up stop signal
STOPSIGNAL SIGTERM

# Set our testing system as entry point
ENTRYPOINT ["python3"]
