FROM python:3.10.4-slim-buster

# Trick to allow source
#RUN rm /bin/sh && ln -s /bin/bash /bin/sh
SHELL ["/bin/bash", "-c"]

USER root

# Todo: Install the basics
RUN apt-get update -y && \
    apt-get install git -y &&\
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
ENV C_FORCE_ROOT=1
ENV NODE_OPTIONS=--openssl-legacy-provider

#export NODE_OPTIONS=--openssl-legacy-provider

# Todo: Create web user
ENV USER www-data
#RUN groupadd --system -g 1000 $USER && \
#    useradd --system -u 1000 -g 1000 --no-create-home $USER



WORKDIR /var/log/rpgsessions
WORKDIR /srv/

# Todo: Prepare web directories
RUN mkdir incoming && \
    mkdir rpgsessions_static && \
    mkdir rpgsessions_media && \
    chown -R $USER:$USER .

WORKDIR /srv/rpgsessions_static
COPY ./docker/rpgsessions/favicon.ico .

# Todo: copy source code and scripts to be used by docker or suited for configuration purpose
WORKDIR /rpgsessions
COPY ./rpgsessions/ .
COPY ./docker/rpgsessions/create_rpgsessions_superuser.py ./rpgsessions/.
COPY ./docker/rpgsessions/settings.py ./rpgsessions/.
COPY ./docker/rpgsessions/wsgi.py ./rpgsessions/.
COPY ./docker/rpgsessions/rpgsessions_entrypoint.sh .

# Todo: install the requirements + gunicorn
RUN pip install pip --upgrade && \
    pip install -r ./requirements.txt && \
    pip install gunicorn && \
    rm -rf /root/.cache/pip/

WORKDIR /rpgsessions

# Todo: At this point, it's a typical rpgsessions commands sequence, supposedly redis/rabbit/celery should be up...
ENTRYPOINT [ "/rpgsessions/rpgsessions_entrypoint.sh" ]