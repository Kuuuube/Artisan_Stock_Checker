import datetime
import json
import os
import time
import traceback

import config_handler
import logger
import stock_checker
import stock_state_handler

utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

artisan_fx_url = "https://artisan-jp.com/global/products/ninja-fx-series.html"
artisan_classic_url = "https://artisan-jp.com/global/products/classic-series.html"
artisan_accessories_url = "https://artisan-jp.com/global/products/accessories.html"

CONFIG_DIR = os.environ.get("ARTISAN_STOCK_CHECKER_CONFIG_DIR", ".")
if CONFIG_DIR and os.path.exists(CONFIG_DIR):
    config_file = os.path.join(CONFIG_DIR, "config.cfg")
    stock_state_file = os.path.join(CONFIG_DIR, "stock_state.json")
else:
    config_file = config_handler.DEFAULT_CONFIG_FILE_PATH
    stock_state_file = stock_state_handler.DEFAULT_STOCK_STATE_FILE_PATH

STOCK_RECORD_DIRECTORY = os.path.dirname(__file__) + "/stock_record/"

stock_delay = float(config_handler.read(config_file, "stock", "stock_delay"))
batch_delay = float(config_handler.read(config_file, "stock", "batch_delay"))
request_fail_delay = float(config_handler.read(config_file, "stock", "request_fail_delay"))

def safe_write_stock_json(json_file_name: str, json_data: dict) -> None:
    try:
        os.makedirs(STOCK_RECORD_DIRECTORY, exist_ok = True)
        with open(STOCK_RECORD_DIRECTORY + json_file_name, "w") as json_file:
            json.dump(json_data, json_file)
    except Exception:  # noqa: BLE001
        logger.error_log("Failed to write json:", traceback.format_exc())

while True:
    try:
        current_epoch_time_ms_str = str(int(datetime.datetime.now(tz = datetime.timezone.utc).timestamp() * 1000))

        full_stock_data = stock_checker.get_stock_data(artisan_fx_url, request_fail_delay)
        safe_write_stock_json("full_stock_data_" + current_epoch_time_ms_str, full_stock_data)

        product_infos = stock_checker.parse_stock_data(full_stock_data)
        safe_write_stock_json("product_infos_" + current_epoch_time_ms_str, full_stock_data)

        for sku, product_info in product_infos.items():
            stock_state_handler.write_state_file(sku, product_info)

        time.sleep(stock_delay)
    except Exception:  # noqa: BLE001, PERF203
        logger.error_log("Critical failure in stock_check_runner:", traceback.format_exc())
