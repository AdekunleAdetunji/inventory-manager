FROM python:3.10.15-bullseye

LABEL Author="ProjectMonty" email="adekunleadetunjiwilson@gmail.com" github="https://github.com/AdekunleAdetunji" version="1.0"

WORKDIR /home/user/app

COPY ./requirements.txt .

RUN ["pip", "install", "-r", "requirements.txt"]