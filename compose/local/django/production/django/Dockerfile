FROM python:3.9-alpine3.13
LABEL maintainer="thejuni96"

ENV PYTHONUNBUFFERED 1

COPY ./requirements /tmp/requirements
COPY ./goal_maven /goal_maven
WORKDIR /goal_maven
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements/base.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.local.txt ; \
        else /py/bin/pip install -r /tmp/requirements.production.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user