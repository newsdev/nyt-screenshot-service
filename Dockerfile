
FROM markadams/chromium-xvfb-py3

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        git\
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install uwsgi

COPY requirements.txt /usr/src/app/
RUN pip3 install -r /usr/src/app/requirements.txt
COPY . /usr/src/app/

ENV PYTHONPATH=/usr/src/app

EXPOSE 80