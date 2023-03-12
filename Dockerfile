ARG PYTHON_VERSION=3.10-slim-buster

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    pip install dj-database-url==1.2.0 psycopg2-binary==2.9.5 && \
    rm -rf /root/.cache/

COPY helpdesk/ /code/
COPY helpdesk/helpdesk/configuration.docker.py /code/helpdesk/configuration.py

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "helpdesk.wsgi"]
