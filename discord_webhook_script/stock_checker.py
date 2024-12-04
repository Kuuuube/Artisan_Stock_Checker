import requests
import re
import traceback
import error_logger

request_url = "https://www.artisan-jp.com/get_syouhin.php"
cart_url = "https://www.artisan-jp.com/stock_recheck.php"


def cart_check_func(stock_check, request_fail_delay=240):
    try:
        # what this witchcraft does:
        # takes for example this: 4562332172443/FX-HI-XS-S-R/HIEN FX XSOFT S Wine red/2100.0/1/XSOFT/
        # and makes it into this: 4562332172443,FX-HI-XS-S-R HIEN FX XSOFT S Wine red,1,2100.0,1
        split_request = stock_check.split("/")
        split_request[1] = split_request[1] + " " + split_request[2]
        split_request[2] = "1"
        del split_request[5]
        del split_request[5]
        combined_request = ",".join(split_request)

        cookies = {
            "cart": combined_request,
            "disc": "1",
            "lung": "jpf",
            "souryou": "800,SAL",
        }

        # delay before request due to check cart being called right after the stock check request
        add_to_cart = requests.post(
            cart_url, cookies=cookies, timeout=request_fail_delay
        )

        if combined_request == add_to_cart.text:
            return "True"
        else:
            return "False"

    except Exception:
        error_logger.error_log("Cart check failed:", traceback.format_exc())
        return "Request failed"


def stock_check_func(request_data, request_fail_delay=240):
    data = {
        "kuni": "on",  # this uses the english site and is required for cart check to work in a simple way
        "sir": request_data[0] + request_data[1],
        "size": request_data[2],
        "color": request_data[3],
    }
    try:
        stock_check = requests.post(request_url, data, timeout=request_fail_delay)
        stock_regex = re.search("^[0-z]+(?=\/)", stock_check.text)
        # in stock example: 4562332172443/FX-HI-XS-S-R/HIEN FX XSOFT S Wine red/2100.0/1/XSOFT/
        # out of stock example: NON/FX-HI-SF-XL-R/HIEN FX XSOFT S Wine red/2100.0/1/XSOFT/
        # out of stock example2: SELECT jan,model,sir,sir_eng,`in`,`out`,price,sale_price,kaigai_price,size,hardness FROM kai_price_local WHERE sir_id = 150 AND size = 3 AND color = 5

        # out of stock and not in production (example2)
        if stock_regex == None:
            return ["False"]

        # in stock
        elif stock_regex.group(0) != "NON":
            return ["True", stock_check.text]

        # out of stock
        else:
            return ["False"]

    except Exception:
        error_logger.error_log("Stock check failed:", traceback.format_exc())
        return ["Request failed"]
