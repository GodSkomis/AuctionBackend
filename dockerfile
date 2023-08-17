FROM python:slim-bullseye

RUN pip install --upgrade pip
WORKDIR /app
COPY . /app

ARG DJANGO_ALLOWED_HOSTS_ARG
ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS_ARG

RUN pip install -r reqs.txt

RUN python manage.py makemigrations