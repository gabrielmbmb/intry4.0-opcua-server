ARG PYTHON_VERSION=3.8-slim
FROM python:${PYTHON_VERSION}

LABEL maintainer="gmartin_b@usal.es"

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install pipenv

ADD Pipfile /tmp
RUN cd /tmp && \
    pipenv lock --requirements > requirements.txt

RUN pip install -r /tmp/requirements.txt
ADD . /tmp/app

RUN pip install /tmp/app

CMD ["intry-opcua"]