import datetime
import json
import os
import time
import traceback

import config_handler
import logger
import stock_checker
import stock_state_handler
import webhook_assembler
import webhook_handler

utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

# all of these pages max out at 25 products
# if artisan ever has more products, scraping multiple pages will need to be added (not skus, product variations dont count)
artisan_all_products_url = "https://artisan-jp.com/global/products?product_list_limit=25"
artisan_fx_url = "https://artisan-jp.com/global/products/ninja-fx-series?product_list_limit=25"
artisan_classic_url = "https://artisan-jp.com/global/products/classic-series?product_list_limit=25"
artisan_accessories_url = "https://artisan-jp.com/global/products/accessories?product_list_limit=25"

config_file_path = config_handler.DEFAULT_CONFIG_FILE_PATH
stock_state_file_path = stock_state_handler.DEFAULT_STOCK_STATE_FILE_PATH

CONFIG_DIR = os.environ.get("ARTISAN_STOCK_CHECKER_CONFIG_DIR", ".")
if CONFIG_DIR and os.path.exists(CONFIG_DIR):
    config_file_path = os.path.join(CONFIG_DIR, "config.cfg")
    stock_state_file_path = os.path.join(CONFIG_DIR, "stock_state.json")

STOCK_RECORD_DIRECTORY = os.path.dirname(__file__) + "/stock_record/"

stock_delay = float(config_handler.read(config_file_path, "stock", "stock_delay"))
batch_delay = float(config_handler.read(config_file_path, "stock", "batch_delay"))
request_fail_delay = float(config_handler.read(config_file_path, "stock", "request_fail_delay"))
webhook_send_delay = float(config_handler.read(config_file_path, "webhook", "webhook_send_delay"))

uptime_webhook_url = config_handler.read(config_file_path, "webhook", "uptime_url")
critical_error_webhook_url = config_handler.read(config_file_path, "webhook", "critical_error_url")

request_headers_override = config_handler.read(config_file_path, "stock", "request_headers_override")
request_headers_override = json.loads(request_headers_override) if len(request_headers_override) > 0 else None

def safe_write_stock_json(json_file_name: str, json_data: dict) -> None:
    try:
        os.makedirs(STOCK_RECORD_DIRECTORY, exist_ok = True)
        with open(STOCK_RECORD_DIRECTORY + json_file_name, "w") as json_file:
            json.dump(json_data, json_file)
    except Exception:  # noqa: BLE001
        logger.error_log("Failed to write json:", traceback.format_exc())

#send bot started notification to uptime webhook
utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
webhook_handler.send_unhandled_webhook(uptime_webhook_url, request_fail_delay, data = {"content": "","embeds": [{"title": "Bot started","description": utc_time}]})

while True:
    try:
        current_epoch_time_ms_str = str(int(datetime.datetime.now(tz = datetime.timezone.utc).timestamp() * 1000))

        full_stock_data = stock_checker.get_stock_data(artisan_all_products_url, request_fail_delay, request_headers_override)
        safe_write_stock_json("full_stock_data_" + current_epoch_time_ms_str + ".json", full_stock_data)

        product_infos = stock_checker.parse_stock_data(full_stock_data)
        safe_write_stock_json("product_infos_" + current_epoch_time_ms_str + ".json", product_infos)
        del product_infos["skuless_products"] # ignore skuless products list

        for sku, product_info in product_infos.items():
            previously_in_stock = stock_state_handler.find_item_state(sku, product_info, stock_state_file_path)
            if not previously_in_stock and product_info["in_stock"]:
                webhook_handler.send_webhook(webhook_assembler.get_webhook_url(product_info), webhook_assembler.assemble_webhook(product_info), webhook_send_delay, request_fail_delay)
                time.sleep(webhook_send_delay)

        utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

        logger.log(utc_time + " Batch complete, waiting: " + str(batch_delay) + " seconds")
        webhook_handler.send_unhandled_webhook(uptime_webhook_url, request_fail_delay, data = {"content": "","embeds": [{"title": "Batch complete","description": utc_time}]})

        time.sleep(batch_delay)
    except Exception:  # noqa: BLE001, PERF203
        try:
            logger.error_log("Crash in main process, attempting to recover in " + str(batch_delay) + " seconds", traceback.format_exc())
            critical_error_webhook_data = {"content": "","embeds": [{"title": "Crash in main process","description": "Attempting to recover in " + str(batch_delay) + " seconds\n```\n" + str(traceback.format_exc())[:2048] + "\n```"}]}
            webhook_handler.send_unhandled_webhook(critical_error_webhook_url, request_fail_delay, critical_error_webhook_data)
            time.sleep(batch_delay)
        except Exception:  # noqa: BLE001
            logger.error_log("Crash in main process, failed to send critical error webhook", traceback.format_exc())
            time.sleep(batch_delay)
