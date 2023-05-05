FROM python:3.9-alpine3.13
LABEL maintainer="thejuni96"

ENV PYTHONUNBUFFERED 1

COPY ./requirements /tmp/requirements
COPY ./goal_maven /Goal-Maven/goal_maven
COPY ./config /Goal-Maven/config
COPY ./manage.py /Goal-Maven/manage.py
COPY ./setup.cfg /Goal-Maven/setup.cfg
WORKDIR /Goal-Maven
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements/base.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements/local.txt ; \
        else /py/bin/pip install -r /tmp/requirements/production.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    chown -R django-user:django-user /Goal-Maven
    #chown -R django-user:django-user /py/lib

ENV PATH="/py/bin:$PATH"

USER django-user