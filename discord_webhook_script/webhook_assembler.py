import datetime

import config_handler

DEFAULT_ARTISAN_URL = "https://artisan-jp.com/global/"

def assemble_webhook(product_info: dict) -> dict:
    utc_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "content": get_role_ping(product_info) + " In Stock!",
        "embeds": [
            {
                "title": safe_dict_index(product_info, "product_name", "Unknown Product"),
                "url": safe_dict_index(product_info, "product_link", DEFAULT_ARTISAN_URL),
                "fields": [
                    {
                    "name": assemble_embed_field(product_info),
                    "value": "",
                    },
                ],
                "thumbnail": {
                    "url": safe_dict_index(product_info, "thumbnail", ""),
                },
                "footer": {
                    "text": utc_time,
                },
                "color": get_int_color(product_info),
            },
        ],
    }


def assemble_embed_field(product_info: dict) -> str:
    assembled_string = ""
    exposed_details = {"product_name": "Model", "base_type": "Hardness", "size": "Size", "color": "Color", "price": "Price"}
    details_strings = []
    for exposed_key, exposed_string in exposed_details.items():
        if exposed_key in product_info:
            details_strings.append(exposed_string + ": " + product_info[exposed_key].strip())

    assembled_string += "\n".join(details_strings)

    return assembled_string


def get_webhook_url(product_info: dict) -> str:
    webhook_url_key = ""
    size_mappings = {
        "S": "s_url",
        "M": "m_url",
        "L": "l_url",
        "XL": "xl_url",
        "XXL": "xxl_url",
    }
    if "size" in product_info:
        webhook_url_key = safe_dict_index(size_mappings, product_info["size"], "fallback_url")
    else:
        webhook_url_key = "na_url"

    webhook_url = config_handler.read(config_handler.DEFAULT_CONFIG_FILE_PATH, "webhook", webhook_url_key)
    if webhook_url == "":
        webhook_url = config_handler.read(config_handler.DEFAULT_CONFIG_FILE_PATH, "webhook", "fallback_url")

    return webhook_url


def get_role_ping(product_info: dict) -> str:
    product_name_mappings = {
        "ZERO CLASSIC": "role_cs_zero",
        "RAIDEN CLASSIC": "role_cs_raiden",
        "NINJA FX HAYATE-OTSU": "role_fx_hayate_otsu",
        "NINJA FX HAYATE-OTSU V2": "role_fx_hayate_otsu_v2",
        "NINJA FX HAYATE-KOU": "role_fx_hayate_kou",
        "NINJA FX HIEN": "role_fx_hien",
        "NINJA FX ZERO": "role_fx_zero",
        "NINJA FX RAIDEN": "role_fx_raiden",
        "NINJA FX SHIDENKAI V2": "role_fx_shidenkai",
        "NINJA FX TYPE-99": "role_fx_type99",
        "NINJA FX KEY-83": "role_fx_key83",
        "MIZUGUMO FUTAE-P8": "role_skates",
        "Mousepad Sweeper MS-01": "role_misc",
    }
    config_key = safe_dict_index(product_name_mappings, safe_dict_index(product_info, "product_name", ""), "Unknown Product")
    return config_handler.read(config_handler.DEFAULT_CONFIG_FILE_PATH, "webhook_role_pings", config_key)


def get_int_color(product_info: dict) -> int:
    if "hex_color" not in product_info:
        return None

    return int(product_info["hex_color"].replace("#", ""), 16)


def safe_dict_index(dictionary: dict, key: str, default):  # noqa: ANN001, ANN201
    try:
        return dictionary[key]
    except KeyError:
        return default
