import json
import os
import re

import logger
import requests

def get_stock_data(url: str, request_timeout: int, request_headers_override: dict) -> dict:
    response = requests.get(url, timeout = request_timeout, headers = request_headers_override)

    response_text_stripped = response.text.replace("\n", "").replace("\r", "")
    product_containers = re.findall('<li class="item product product-item">.*?</li>', response_text_stripped)
    magento_swatch_stock_data_jsons = []
    single_sku_stock_data_dicts = []
    skuless_products = []
    for product_container in product_containers:
        magento_jsons = re.findall('(?<=<script type="text/x-magento-init">).*?(?=</script>)', product_container)
        product_link_container = re.search('<a class="product-item-link".*?</a>', product_container)[0]
        product_name = re.search("(?<=>).*?(?=<)", product_link_container)[0].strip()
        product_link = re.search('(?<=href=").*?(?=")', product_link_container)[0].strip()

        # product with no selectable options, single sku
        if (len(magento_jsons) == 0):
            in_stock = re.search("Add( |&#x20;)to( |&#x20;)Cart", product_container)
            out_of_stock = re.search("(Out of stock|stock unavailable)", product_container)
            if (bool(in_stock) == bool(out_of_stock)):
                logger.log("Single sku in stock and out of stock match, in_stock: " + str(in_stock) + ", out_of_stock: " + str(out_of_stock))

            sku_search = re.search('(?<=data-product-sku=").*?(?=")', product_container)
            if (not sku_search):
                logger.log("Single sku item failed to find sku, product_container: " + product_container)
                skuless_data = {
                    "product_name": product_name,
                    "product_link": product_link,
                    "in_stock": bool(in_stock),
                }
                skuless_products.append(skuless_data)
                continue

            stock_data = {
                "product_name": product_name,
                "product_link": product_link,
                "sku": sku_search[0],
                "in_stock": bool(in_stock),
            }

            single_sku_stock_data_dicts.append(stock_data)

        for magento_json in magento_jsons:
            magento_json_parsed = json.loads(magento_json)
            for key in magento_json_parsed:
                if "[data-role=swatch-option-" in key:
                    truncated_magento_json = magento_json_parsed[key]["Magento_Swatches/js/swatch-renderer"]
                    truncated_magento_json["product_name"] = product_name
                    truncated_magento_json["product_link"] = product_link
                    magento_swatch_stock_data_jsons.append(truncated_magento_json)

    return {
        "magento_swatch_stock_data": magento_swatch_stock_data_jsons,
        "single_sku_stock_data_dicts": single_sku_stock_data_dicts,
        "skuless_products": skuless_products,
    }


def parse_stock_data(full_stock_data: dict) -> dict:
    product_info_dict = {}

    for magento_swatch_stock_data_json in full_stock_data["magento_swatch_stock_data"]:
        attributes = magento_swatch_stock_data_json["jsonConfig"]["attributes"]
        for attribute_value in attributes.values():
            attribute_code = attribute_value["code"] # name of attribute
            for option in attribute_value["options"]:
                option_label = option["label"]
                option_id = option["id"]
                for product_id in option["products"]:
                    if product_id in product_info_dict:
                        product_info_dict[product_id][attribute_code] = option_label
                        product_info_dict[product_id][attribute_code + "_id"] = option_id
                    else:
                        product_info_dict[product_id] = {
                            "product_id": product_id,
                            "product_name": magento_swatch_stock_data_json["product_name"],
                            "product_link": magento_swatch_stock_data_json["product_link"],
                            attribute_code: option_label,
                            attribute_code + "_id": option_id,
                            # set defaults
                            "in_stock": False,
                            "sku": "",
                            "price": 0,
                        }

        salable = magento_swatch_stock_data_json["jsonConfig"]["salable"]
        for salable_value in salable.values():
            for product_ids in salable_value.values():
                for product_id in product_ids:
                    if product_id in product_info_dict:
                        product_info_dict[product_id]["in_stock"] = True

        option_prices = magento_swatch_stock_data_json["jsonConfig"]["optionPrices"]
        price_pattern = magento_swatch_stock_data_json["jsonConfig"]["priceFormat"]["pattern"]
        for product_id, prices in option_prices.items():
            if product_id in product_info_dict:
                product_info_dict[product_id]["price"] = price_pattern.replace(r"%s", str(prices["finalPrice"]["amount"]))

        swatch_config = magento_swatch_stock_data_json["jsonSwatchConfig"]
        for _attribute_id, attribute_swatch_info in swatch_config.items():
            for product_id in product_info_dict:
                if "color_id" in product_info_dict[product_id] and product_info_dict[product_id]["color_id"] in attribute_swatch_info:
                    product_info_dict[product_id]["hex_color"] = attribute_swatch_info[product_info_dict[product_id]["color_id"]]["value"]

        # switch from product id sorted to sku last due to id use within magento json
        skus = magento_swatch_stock_data_json["jsonConfig"]["sku"]
        for product_id, sku in skus.items():
            if product_id in product_info_dict:
                product_info_dict[product_id]["sku"] = sku
                product_info_dict[sku] = product_info_dict[product_id]
                del product_info_dict[product_id]

    for single_sku_stock_data_dict in full_stock_data["single_sku_stock_data_dicts"]:
        product_info_dict[single_sku_stock_data_dict["sku"]] = single_sku_stock_data_dict

    product_info_dict["skuless_products"] = full_stock_data["skuless_products"]

    return product_info_dict
