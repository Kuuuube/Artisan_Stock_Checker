FROM python:3.10

ENV CONFIG_PATH=/config

RUN pip install --no-cache-dir requests

RUN mkdir -p /app/discord_webhook_script /config
COPY discord_webhook_script /app/discord_webhook_script
WORKDIR /app/discord_webhook_script

RUN chmod 755 /app /config

CMD ["python3", "check_artisan_stock_webhook.py"]