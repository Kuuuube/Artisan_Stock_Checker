FROM python:3.10

ENV CONFIG_PATH=/config
ENV PUID=1000
ENV PGID=1001

RUN pip install --no-cache-dir requests

RUN mkdir -p /app/discord_webhook_script /config
COPY discord_webhook_script /app/discord_webhook_script
WORKDIR /app/discord_webhook_script

RUN groupadd -g ${PGID} appgroup && \
    useradd -u ${PUID} -g appgroup appuser
# Set permissions
RUN chown -R ${PUID}:${PGID} /app /config

USER ${PUID}:${PGID}
CMD ["python3", "check_artisan_stock_webhook.py"]