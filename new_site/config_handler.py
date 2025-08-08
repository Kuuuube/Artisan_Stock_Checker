import configparser
import hashlib
import os
import time
import traceback

import logger

DEFAULT_CONFIG_FILE_PATH = os.path.dirname(__file__) + "/config.cfg"

DEFAULT_CONFIG = {
    "stock": {
        "stock_delay": "10",
        "batch_delay": "300",
        "request_fail_delay": "120",
    },
    "webhook": {
        "webhook_send_delay": "1",
        "fallback_url": "",
        "S_url": "",
        "M_url": "",
        "L_url": "",
        "XL_url": "",
        "XXL_url": "",
        "na_url": "",
        "content": "{Role Ping} In Stock!\\nModel: {Model}, Hardness: {Hardness}, Size: {Size}, Color: {Color}\\nLink: {Link}",
        "uptime_url": "",
        "critical_error_url": "",
    },
    "webhook_role_pings": {
        "role_CS_Zero": "<@&>",
        "role_CS_Raiden": "<@&>",
        "role_FX_Hayate_Otsu": "<@&>",
        "role_FX_Hayate_Otsu_V2": "<@&>",
        "role_FX_Hayate_Kou": "<@&>",
        "role_FX_Hien": "<@&>",
        "role_FX_Zero": "<@&>",
        "role_FX_Raiden": "<@&>",
        "role_FX_Shidenkai": "<@&>",
        "role_FX_TYPE99": "<@&>",
        "role_FX_KEY83": "<@&>",
        "role_skates": "<@&>",
    },
}

def get_config_parser(config_file_path: str = DEFAULT_CONFIG_FILE_PATH) -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config


def backup_bad_config(config_file_path: str = DEFAULT_CONFIG_FILE_PATH) -> None:
    try:
        hash_value = ""
        with open(config_file_path, "rb") as hashfile:
            hash_value = hashlib.md5(hashfile.read(), usedforsecurity = False).hexdigest()
        backup_file = config_file_path + ".bak" + hash_value
        with open(config_file_path) as config_file, open(backup_file, "w") as backup:
            backup.writelines(config_file)
    except Exception:  # noqa: BLE001
        logger.error_log("Failed to backup config: ", traceback.format_exc())


def default_config(config_file_path: str = DEFAULT_CONFIG_FILE_PATH) -> None:
    backup_bad_config(config_file_path)

    defaults = configparser.ConfigParser()
    for key in DEFAULT_CONFIG:
        defaults[key] = DEFAULT_CONFIG[key]

    with open(config_file_path, "w") as conf:
        defaults.write(conf)


def read(config_file_path: str, section: str, name: str) -> str:
    while True:
        try:
            config_parser = get_config_parser(config_file_path)
            return config_parser.get(section, name)

        except Exception:  # noqa: BLE001, PERF203
            logger.error_log("Config corrupted. Reverting to default:", traceback.format_exc())
            default_config(config_file_path)
            time.sleep(1)

    return None


def write(config_file_path: str, section: str, name: str, value: str) -> None:
    while True:
        try:
            config_parser = get_config_parser(config_file_path)
            if not config_parser.has_section(section):
                config_parser.add_section(section)
            config_parser[section][name] = value
            with open(config_file_path, "w") as conf:
                config_parser.write(conf)
            break
        except Exception:  # noqa: BLE001
            logger.error_log("Config corrupted. Reverting to default:", traceback.format_exc())
            default_config(config_file_path)
            time.sleep(1)
