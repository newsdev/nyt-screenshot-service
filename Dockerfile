
FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        wget unzip chromium\
    && rm -rf /var/lib/apt/lists/*

RUN wget https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN chmod +x chromedriver
RUN cp chromedriver /usr/bin/chromedriver

RUN pip install uwsgi

COPY requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt
COPY . /usr/src/app/

ENV PYTHONPATH=/usr/src/app

EXPOSE 80