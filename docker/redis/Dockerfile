FROM redis:5.0-bullseye

WORKDIR /usr/local/etc/redis/
COPY ./docker/redis/redis_light.conf ./redis.conf

CMD [ "redis-server", "/usr/local/etc/redis/redis.conf"]