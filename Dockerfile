FROM python:3.12-slim-bullseye

LABEL MAINTAINER="Pradeep Bashyal"

WORKDIR /app

ARG PY_ARD_VERSION=1.5.2

COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY requirements-deploy.txt /app
RUN pip install --no-cache-dir -r requirements-deploy.txt

RUN pip install --no-cache-dir py-ard==$PY_ARD_VERSION

COPY app.py /app/
COPY api.py /app/
COPY api-spec.yaml /app/

COPY docker-entrypoint-flask.sh /usr/local/bin/
CMD ["/usr/local/bin/docker-entrypoint-flask.sh"]
