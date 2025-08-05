import requests
import re
import json

artisan_fx_url = "https://artisan-jp.com/global/products/ninja-fx-series.html"
artisan_cert_path = "www-artisan-jp-com.pem" # shim due to requests not recognizing `GlobalSign nv-sa` cert
response = requests.get(artisan_fx_url, verify = artisan_cert_path)

response_text_stripped = response.text.replace("\n", "").replace("\r", "")
magneto_init_jsons = re.findall('(?<=<script type=\\"text/x-magento-init\\">).*?(?=</script>)', response_text_stripped)
stock_magneto_jsons = []
for magneto_init_json in magneto_init_jsons:
    magneto_json_parsed = json.loads(magneto_init_json)
    for key in magneto_json_parsed.keys():
        if "[data-role=swatch-option-" in key:
            stock_magneto_jsons.append(magneto_json_parsed[key]["Magento_Swatches/js/swatch-renderer"])


product_info_dict = {}
def init_product_info_dict(stock_magneto_json):
    global product_info_dict
    attributes = stock_magneto_json["jsonConfig"]["attributes"]
    for attribute_value in attributes.values():
        attribute_code = attribute_value["code"] # name of attribute
        for option in attribute_value["options"]:
            option_label = option["label"]
            for product_id in option["products"]:
                if product_id in product_info_dict:
                    product_info_dict[product_id][attribute_code] = option_label
                else:
                    product_info_dict[product_id] = {
                        attribute_code: option_label,
                        # set defaults
                        "in_stock": False,
                        "sku": "",
                        "price": 0,
                    }

    salable = stock_magneto_json["jsonConfig"]["salable"]
    for salable_value in salable.values():
        for product_ids in salable_value.values():
            for product_id in product_ids:
                if product_id in product_info_dict:
                    product_info_dict[product_id]["in_stock"] = True

    skus = stock_magneto_json["jsonConfig"]["sku"]
    for product_id, sku in skus.items():
        if product_id in product_info_dict:
            product_info_dict[product_id]["sku"] = sku

    option_prices = stock_magneto_json["jsonConfig"]["optionPrices"]
    for product_id, prices in option_prices.items():
        if product_id in product_info_dict:
            product_info_dict[product_id]["price"] = prices["finalPrice"]["amount"]

for stock_magneto_json in stock_magneto_jsons:
    init_product_info_dict(stock_magneto_json)

print(json.dumps(product_info_dict))

