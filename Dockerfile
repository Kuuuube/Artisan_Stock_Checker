FROM lscr.io/linuxserver/baseimage-alpine:latest

ENV CONFIG_PATH=/config

# Install Python 3 and required packages
RUN \
    apk add --no-cache python3 py3-pip && \
    pip3 install --no-cache-dir requests

COPY discord_webhook_script /app/discord_webhook_script

RUN \
    chown -R $PUID:$PGID /app /config

WORKDIR /app/discord_webhook_script

USER $PUID:$PGID

CMD ["python3", "check_artisan_stock_webhook.py"]
