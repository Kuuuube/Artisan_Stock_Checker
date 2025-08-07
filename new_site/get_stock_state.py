import requests
import re
import json

def get_raw_stock_data():
    artisan_fx_url = "https://artisan-jp.com/global/products/ninja-fx-series.html"
    artisan_cert_path = "www-artisan-jp-com.pem" # shim due to requests not recognizing `GlobalSign nv-sa` cert
    response = requests.get(artisan_fx_url, verify = artisan_cert_path)

    response_text_stripped = response.text.replace("\n", "").replace("\r", "")
    product_containers = re.findall('<li class="item product product-item">.*?</li>', response_text_stripped)
    raw_stock_data_jsons = []
    for product_container in product_containers:
        magento_jsons = re.findall('(?<=<script type="text/x-magento-init">).*?(?=</script>)', product_container)
        product_link_container = re.search('<a class="product-item-link".*?</a>', product_container)[0]
        product_name = re.search('(?<=>).*?(?=<)', product_link_container)[0].strip()
        product_link = re.search('(?<=href=").*?(?=")', product_link_container)[0].strip()
        for magento_json in magento_jsons:
            magento_json_parsed = json.loads(magento_json)
            for key in magento_json_parsed.keys():
                if "[data-role=swatch-option-" in key:
                    truncated_magento_json = magento_json_parsed[key]["Magento_Swatches/js/swatch-renderer"]
                    truncated_magento_json["product_name"] = product_name
                    truncated_magento_json["product_link"] = product_link
                    raw_stock_data_jsons.append(truncated_magento_json)

    return raw_stock_data_jsons

def get_product_info():
    product_info_dict = {}

    raw_stock_data_jsons = get_raw_stock_data()
    for raw_stock_data_json in raw_stock_data_jsons:
        attributes = raw_stock_data_json["jsonConfig"]["attributes"]
        for attribute_value in attributes.values():
            attribute_code = attribute_value["code"] # name of attribute
            for option in attribute_value["options"]:
                option_label = option["label"]
                for product_id in option["products"]:
                    if product_id in product_info_dict:
                        product_info_dict[product_id][attribute_code] = option_label
                    else:
                        product_info_dict[product_id] = {
                            "product_name": raw_stock_data_json["product_name"],
                            "product_link": raw_stock_data_json["product_link"],
                            attribute_code: option_label,
                            # set defaults
                            "in_stock": False,
                            "sku": "",
                            "price": 0,
                        }

        salable = raw_stock_data_json["jsonConfig"]["salable"]
        for salable_value in salable.values():
            for product_ids in salable_value.values():
                for product_id in product_ids:
                    if product_id in product_info_dict:
                        product_info_dict[product_id]["in_stock"] = True

        skus = raw_stock_data_json["jsonConfig"]["sku"]
        for product_id, sku in skus.items():
            if product_id in product_info_dict:
                product_info_dict[product_id]["sku"] = sku

        option_prices = raw_stock_data_json["jsonConfig"]["optionPrices"]
        for product_id, prices in option_prices.items():
            if product_id in product_info_dict:
                product_info_dict[product_id]["price"] = prices["finalPrice"]["amount"]

    return product_info_dict
