
FROM markadams/chromium-xvfb-py3

RUN apt-get update
RUN apt-get install git

RUN pip3 install uwsgi

COPY requirements.txt /usr/src/app/
RUN pip3 install -r /usr/src/app/requirements.txt
COPY . /usr/src/app/

ENV PYTHONPATH=/usr/src/app

EXPOSE 80