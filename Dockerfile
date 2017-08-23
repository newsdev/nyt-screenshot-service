
FROM python:3.6

RUN umount -l /dev/shm
RUN umount -l /tmp
RUN mount -t tmpfs -o size=256m tmpfs /dev/shm
RUN mount -t tmpfs -o size=1024m tmpfs /tmp

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromedriver \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/lib/chromium/chromedriver /usr/bin/chromedriver
RUN pip install uwsgi

COPY requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt
COPY . /usr/src/app/

ENV PYTHONPATH=/usr/src/app

EXPOSE 80
CMD ["/usr/local/bin/uwsgi", "--ini", "/usr/src/app/config/prd/app.ini"]
