import json
import time
import hashlib
import traceback
import error_logger


def backup_bad_states(json_file):
    try:
        with open(json_file, "rb") as hashfile:
            bytes = hashfile.read()
            hash_value = hashlib.md5(bytes).hexdigest()
        with open(json_file, "r") as jsonfile, open(
            json_file + ".bak" + hash_value, "w"
        ) as backup:
            for line in jsonfile:
                backup.write(line)

    except Exception:
        pass


def default_json(json_file):
    backup_bad_states(json_file)

    with open(json_file, "w") as jsonfile:
        json.dump({}, jsonfile)


def read_state_file(json_file, dict_key):
    while True:
        try:
            with open(json_file, "r") as states:
                states_dict = json.load(states)

            if dict_key in states_dict:
                return states_dict[dict_key]

            else:
                states_dict[dict_key] = "False"

                with open(json_file, "w") as states:
                    json.dump(states_dict, states)

                return "False"

        except Exception:
            if json_file == "stock_state.json":
                error_logger.error_log(
                    "Stock states corrupted. Reverting to default:",
                    traceback.format_exc(),
                )
                default_json(json_file)
            time.sleep(1)


def write_state_file(json_file, dict_key, value):
    with open(json_file, "r") as states:
        states_dict = json.load(states)

    states_dict[dict_key] = value

    with open(json_file, "w") as states:
        json.dump(states_dict, states)


def find_item_state(item, stock_state):
    try:
        item_list_combined = "".join(item)

        if stock_state == read_state_file("stock_state.json", item_list_combined):
            return False
        else:
            write_state_file("stock_state.json", item_list_combined, stock_state)
            return True

    except Exception:
        error_logger.error_log(
            "Could not open or write to stock states:", traceback.format_exc()
        )
