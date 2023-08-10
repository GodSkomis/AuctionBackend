from python:slim-bullseye

RUN pip install --upgrade pip
COPY . .

ARG DJANGO_ALLOWED_HOSTS_ARG
ENV DJANGO_ALLOWED_HOSTS=$DJANGO_ALLOWED_HOSTS_ARG

RUN pip install -r reqs.txt