FROM naxa/python:3.9-slim

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code

COPY requirements.txt /code

RUN apt-get update && apt-get install -y \
    binutils libproj-dev gdal-bin postgresql-client

RUN pip install --no-cache-dir setuptools wheel numpy
RUN pip install --no-cache-dir -r /code/requirements.txt
RUN rm /code/requirements.txt

COPY . /code

ENTRYPOINT /code/docker-entrypoint.sh