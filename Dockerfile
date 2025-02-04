# download base docker image
FROM python:3.10.15-bullseye

LABEL Author="ProjectMonty" email="adekunleadetunjiwilson@gmail.com" github="https://github.com/AdekunleAdetunji" version="1.0"

# update the base image
RUN apt-get -yqq update

# set the container working direcctory 
WORKDIR /home/inventory

# copy local requirements.txt file to docker image
COPY ./requirements.txt .

# run command to complete image build
RUN ["pip", "install", "-r", "requirements.txt"]