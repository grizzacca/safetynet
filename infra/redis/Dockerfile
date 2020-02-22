FROM redis:5.0.7
LABEL maintainer="Andrei Titerlea (grizzacca@gmail.com)"

COPY redis.conf /etc/redis/redis.conf

# Their entrypoint script expects that we'll add our custom config
CMD ["/etc/redis/redis.conf"]
