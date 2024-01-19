FROM python:3.11-slim-buster

LABEL MAINTAINER="Pradeep Bashyal"

WORKDIR /app

ARG PY_ARD_VERSION=1.0.10

COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY requirements-deploy.txt /app
RUN pip install --no-cache-dir -r requirements-deploy.txt

RUN pip install --no-cache-dir py-ard==$PY_ARD_VERSION

RUN pyard-import && \
    pyard --version && \
    pyard-status

COPY app.py /app/
COPY api.py /app/
COPY api-spec.yaml /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--worker-tmp-dir", "/dev/shm",  "--timeout", "30", "app:app"]
