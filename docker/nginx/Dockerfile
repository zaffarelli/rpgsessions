FROM debian:buster-slim

#ENV IP_UPSTREAM=${IP_UPSTREAM}
#ENV IP_SERVER=${IP_SERVER}

RUN apt-get update && \
    apt-get -y install nginx ufw vim && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /etc/nginx/sites-available
COPY ./docker/nginx/rpgsessions_nginx.conf .
#RUN rm default


WORKDIR /tmp
RUN touch /tmp/nginx.pid

WORKDIR /etc/nginx
RUN mv nginx.conf old_nginx.conf
COPY ./docker/nginx/nginx.conf .
RUN chown -R www-data:www-data /var/log/nginx && \
    chown -R www-data:www-data /tmp/nginx.pid && \
    chown -R www-data:www-data /var/lib/nginx && \
    chown -R www-data:www-data /srv && \
    chown -R www-data:www-data .

WORKDIR /etc/nginx/sites-enabled
RUN rm -r default && \
    ln -s ../sites-available/rpgsessions_nginx.conf && \
    ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

WORKDIR /srv
COPY ./docker/nginx/index.html .

WORKDIR /etc/nginx/

STOPSIGNAL SIGTERM

USER www-data

CMD [ "nginx", "-g", "daemon off;" ]
