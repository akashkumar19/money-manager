FROM python:3.11-slim-bullseye 

ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /moneymanager

# Set the working directory to /music_service
WORKDIR /moneymanager
# Copy the current directory contents into the container at /music_service
ADD . /moneymanager/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt