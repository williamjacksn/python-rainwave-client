FROM python:3.7.4-alpine3.10

COPY requirements.txt /python-rainwave-client/requirements.txt

RUN /usr/local/bin/pip install --no-cache-dir --requirement /python-rainwave-client/requirements.txt

ENV PYTHONUNBUFFERED="1"

ENTRYPOINT ["/usr/local/bin/python"]

COPY . /python-rainwave-client
WORKDIR /python-rainwave-client
