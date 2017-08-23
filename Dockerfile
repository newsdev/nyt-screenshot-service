
FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromedriver chromium\
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/lib/chromium/chromedriver /usr/bin/chromedriver
RUN pip install uwsgi

COPY requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt
COPY . /usr/src/app/

ENV PYTHONPATH=/usr/src/app

EXPOSE 80