FROM python:3.9.5

RUN apt -y update
RUN apt install -y python3-wheel python3-setuptools python3-pip libpq-dev git
RUN python3 -m pip install Cython tornado

EXPOSE 8080
WORKDIR /app

RUN git clone https://github.com/camptocamp/tilecloud.git /app
RUN python3 -m pip install --no-cache-dir --requirement=/app/requirements.txt
