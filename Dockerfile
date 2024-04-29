FROM python:3.9-alpine3.16

COPY requirements.txt /app/requirements.txt

COPY GES /GES

WORKDIR /GES

EXPOSE 8000

RUN pip install -r /app/requirements.txt

RUN adduser --disabled-password fcg

USER fcg
