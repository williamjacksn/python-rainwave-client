FROM python:3.9.5-alpine3.13

COPY requirements.txt /python-rainwave-client/requirements.txt

RUN /usr/local/bin/pip install --no-cache-dir --requirement /python-rainwave-client/requirements.txt

ENV PYTHONUNBUFFERED="1"

ENTRYPOINT ["/usr/local/bin/python"]
