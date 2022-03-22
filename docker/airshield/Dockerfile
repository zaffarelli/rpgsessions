FROM python:3.6.15-buster

# Trick to allow source
#RUN rm /bin/sh && ln -s /bin/bash /bin/sh
SHELL ["/bin/bash", "-c"]

USER root

# Todo: Install the basics
RUN apt-get update -y && \
    apt-get install systemd -y && \
    apt-get install git -y &&\
    apt-get install vim htop -y &&\
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



WORKDIR /var/log/airshield
WORKDIR /srv/

# Todo: Prepare web directories
RUN mkdir incoming && \
    mkdir airshield_static && \
    mkdir airshield_media && \
    chown -R $USER:$USER .

WORKDIR /srv/airshield_static
COPY ./docker/airshield/favicon.ico .

# Todo: Handling nvm to manage Nodes / NPM
RUN cd ~/ &&\
    git clone https://github.com/nvm-sh/nvm.git .nvm && \
    cd ~/.nvm &&\
    git checkout v0.39.1

# Todo: Nodes, NPM and the funny packagers we need (webpack essentially)
WORKDIR /root
COPY ./docker/airshield/nvm.bashrc .

WORKDIR /root
RUN cp /root/.bashrc /root/.bashrc.rescue &&\
    cat /root/nvm.bashrc >> /root/.bashrc

# nota: yarn is shipped in corepack
RUN source /root/.bashrc &&\
    nvm install node --force &&\
    npm install --global npm@8.4.0 &&\
    npm install --global --force corepack &&\
    npm install --global --force webpack &&\
    npm install --global --force webpack-cli

# Todo: Whitelist the address for vilocify to run properly
WORKDIR /etc/saml/certs/
COPY ./docker/airshield/vilocify/*.pem ./

# Todo: copy source code and scripts to be used by docker or suited for configuration purpose
WORKDIR /cve-aggregation
COPY ./cve-aggregation/ .
COPY ./docker/airshield/create_airshield_superuser.py ./airshield/.
COPY ./docker/airshield/settings.py ./airshield/.
COPY ./docker/airshield/wsgi.py ./airshield/.
COPY ./docker/airshield/airshield_entrypoint.sh .

# Todo: install the requirements + gunicorn
RUN pip install pip --upgrade && \
    pip install -r requirements.txt && \
    pip install gunicorn && \
    rm -rf /root/.cache/pip/

# Todo: let's play with nodes to rebuild our website assets (Yarn/Webpack fun, see dedicated script executed at the end)
WORKDIR /cve-aggregation/
COPY ./docker/airshield/upgrade_prod_env.sh ./scripts/.
RUN chmod a+x ./scripts/upgrade_prod_env.sh
RUN ./scripts/upgrade_prod_env.sh

# Todo: Celery
WORKDIR /etc/sysconfig/celery
COPY ./docker/airshield/sysconfig/celery* ./

# Todo: Here is the place where I cry: the service definitions are CentOS specific... (see init.d directory in cve-aggregation source code)
WORKDIR /etc/init.d
COPY ./cve-aggregation/init.d/* ./

# Todo: do I care about enabling? When a docker dies it is respawn... no hot restart/plug actions to be held
RUN install -d -g www-data -o www-data -m u=rwx,g=srwx,o=rx /var/{run,log}/celery
#     && \
#    systemctl enable celeryd && \
#    systemctl enable celerybeat

WORKDIR /usr/local/bin/
COPY ./docker/airshield/celery_start.sh .
RUN chmod a+x ./celery_start.sh

WORKDIR /cve-aggregation/airshield

# Todo: At this point, it's a typical Airshield commands sequence, supposedly redis/rabbit/celery should be up...
ENTRYPOINT [ "/cve-aggregation/airshield_entrypoint.sh" ]