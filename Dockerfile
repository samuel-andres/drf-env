# Creating image based on alpine
FROM python:3.11-alpine

# Labeling with the authors
LABEL maintainer="samucancld"

# Fixing python printing
ENV PYTHONUNBUFFERED 1

# Installing all python dependencies
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Getting the django project into the docker container
RUN mkdir /src
WORKDIR /src
ADD ./ /src

# Creating user
RUN adduser -D user
USER user
