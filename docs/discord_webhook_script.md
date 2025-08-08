# Discord Webhook Script

## Dependencies

Python 3: [Download link](https://www.python.org/downloads/)

Python `requests` module: To install, enter the following command in cmd or a terminal:

```
pip install requests
```

## Usage

1. Run `./discord_webhook_script/check_artisan_stock_webhook.py` then close it to generate default settings file.

    By default, `config.cfg` is expected to be in the current working directory. If you want to put it somewhere else, set this env var: `ARTISAN_STOCK_CHECKER_CONFIG_DIR`.

2. Open `config.cfg` and add your Discord webhook url for `fallback_url = `. The fallback url is always required even if all size urls are present.

    Optional webhooks:

    Add multiple webhook urls to the different sizes (`s_url`, `m_url`, ...) to send to separate webhooks for pads of the specified size.

    Set `uptime_url` to receive notifications when the bot starts or a batch completes.

    Set `critical_error_url` to receive notifications when the bot hits a critical error.

3. Optionally, edit the delays in `config.cfg` to change the delay in seconds between checking stock, looping batch, sending webhooks, and request fail.

    `stock_delay` adds a delay after sending the stock check request.

    `batch_delay` adds a delay between checking the full list of pads. Only used between the last item in the list and the first item in the list when looping back to the first item.

    `request_fail_delay` adds a delay after a request fails before resuming the sending of requests and acts as the request timeout.

    `webhook_send_delay` adds a delay between sending Discord webhook messages.

4. Run `./discord_webhook_script/check_artisan_stock_webhook.py`

## Troubleshooting

To reset settings to default, delete `config.cfg` and run the script. A new `config.cfg` will be generated with defaults.

To reset stock states and tracking, delete `stock_state.json`. This will remove the current stock data collected by the script. Upon running the script again it will rerecord the stock states. This will cause the script to resend webhook messages for items that had previously been recorded as in stock and have not had a change in state.