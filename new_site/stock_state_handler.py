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


def read_state_file(json_file: str, dict_key: str):
    while True:
        try:
            if not os.path.exists(json_file):
                default_json(json_file)
            with open(json_file) as states:
                states_dict = json.load(states)
            if dict_key in states_dict:
                return states_dict[dict_key]
            else:
                states_dict[dict_key] = "False"
                with open(json_file, "w") as states:
                    json.dump(states_dict, states)
                return "False"
        except Exception:  # noqa: BLE001, PERF203
            logger.error_log("Stock states corrupted. Reverting to default:", traceback.format_exc())
            default_json(json_file)
            time.sleep(1)


def write_state_file(json_file: str, dict_key: str, value: str) -> None:
    while True:
        try:
            states_dict = {}
            with open(json_file) as states:
                states_dict = json.load(states)
            states_dict[dict_key] = value
            with open(json_file, "w") as states:
                json.dump(states_dict, states)
            break
        except Exception:  # noqa: BLE001
            logger.error_log("Could not write to stock states:", traceback.format_exc())
            default_json(json_file)
            time.sleep(1)


def find_item_state(item: str, stock_state: bool, stock_state_file_path: str = DEFAULT_STOCK_STATE_FILE_PATH) -> bool:
    try:
        item_list_combined = "".join(item)
        current_state = read_state_file(stock_state_file_path, item_list_combined)
        if stock_state == current_state:
            return False
        else:
            write_state_file(stock_state_file_path, item_list_combined, stock_state)
            return True

    except Exception:
        logger.error_log("Could not open or write to stock states:", traceback.format_exc())
