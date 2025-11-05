import hashlib
import json
import os
import time
import traceback

import logger

DEFAULT_STOCK_STATE_FILE_PATH = os.path.dirname(__file__) + "/stock_state.json"

def backup_bad_states(stock_state_file_path: str = DEFAULT_STOCK_STATE_FILE_PATH) -> None:
    try:
        hash_value = ""
        with open(stock_state_file_path, "rb") as hashfile:
            hash_value = hashlib.md5(hashfile.read(), usedforsecurity = False).hexdigest()
        backup_file = stock_state_file_path + ".bak" + hash_value
        with open(stock_state_file_path) as jsonfile, open(backup_file, "w") as backup:
            backup.writelines(jsonfile)
    except Exception:  # noqa: BLE001
        logger.error_log("Failed to backup bad states, passing:", traceback.format_exc())


def default_json(stock_state_file_path: str = DEFAULT_STOCK_STATE_FILE_PATH) -> None:
    backup_bad_states(stock_state_file_path)
    with open(stock_state_file_path, "w") as jsonfile:
        json.dump({}, jsonfile)


def read_state_file(dict_key: str, stock_state_file_path: str = DEFAULT_STOCK_STATE_FILE_PATH) -> bool:
    while True:
        try:
            states_dict = {}
            if not os.path.exists(stock_state_file_path):
                default_json(stock_state_file_path)
            with open(stock_state_file_path) as states:
                states_dict = json.load(states)
            if dict_key in states_dict:
                return states_dict[dict_key]
            else:
                return False
        except Exception:  # noqa: BLE001, PERF203
            logger.error_log("Stock states corrupted. Reverting to default:", traceback.format_exc())
            default_json(stock_state_file_path)
            time.sleep(1)


def write_state_file(dict_key: str, value: str, stock_state_file_path: str = DEFAULT_STOCK_STATE_FILE_PATH) -> None:
    while True:
        try:
            states_dict = {}
            with open(stock_state_file_path) as states:
                states_dict = json.load(states)
            states_dict[dict_key] = value
            with open(stock_state_file_path, "w") as states:
                json.dump(states_dict, states)
            break
        except Exception:  # noqa: BLE001
            logger.error_log("Could not write to stock states:", traceback.format_exc())
            default_json(stock_state_file_path)
            time.sleep(1)


def find_item_state(dict_key: str, value: dict, stock_state_file_path: str = DEFAULT_STOCK_STATE_FILE_PATH) -> bool:
    try:
        recorded_stock_state = read_state_file(dict_key, stock_state_file_path)
        write_state_file(dict_key, value, stock_state_file_path)
        if not recorded_stock_state:
            return False
        return recorded_stock_state["in_stock"]

    except Exception:  # noqa: BLE001
        logger.error_log("Could not open or write to stock states:", traceback.format_exc())
