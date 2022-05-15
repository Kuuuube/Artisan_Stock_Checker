import requests
import re
import itertools
import time
from datetime import datetime,timezone
import webhook_handler
import artisan_mousepads
import config_handler
import stock_state_tracker

request_url = "https://www.artisan-jp.com/get_syouhin.php"
cart_url = "https://www.artisan-jp.com/stock_recheck.php"

dict_mousepad_models = artisan_mousepads.mousepad_models()
dict_hardnesses = artisan_mousepads.mousepad_hardnesses()
dict_sizes = artisan_mousepads.mousepad_sizes()
dict_colors = artisan_mousepads.mousepad_colors()

cart = False
stock_delay = config_handler.read("config.cfg","stock","stock_delay")
cart_delay = config_handler.read("config.cfg","stock","cart_delay")
batch_delay = config_handler.read("config.cfg","stock","batch_delay")
request_fail_delay = config_handler.read("config.cfg","stock","request_fail_delay")

utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

def cart_check_func(stock_check):
    try:
        #what this witchcraft does:
        #takes for example this: 4562332172443/FX-HI-XS-S-R/HIEN FX XSOFT S Wine red/2100.0/1/XSOFT/
        #and makes it into this: 4562332172443,FX-HI-XS-S-R HIEN FX XSOFT S Wine red,1,2100.0,1
        split_request = stock_check.split("/")
        split_request[1] = split_request[1] + " " + split_request[2]
        split_request[2] = "1"
        del split_request[5]
        del split_request[5]
        combined_request = ",".join(split_request)
        
        cookies = {"cart":combined_request, "disc": "1", "lung": "jpf", "souryou": "800,SAL"}

        #delay before request due to check cart being called right after the stock check request
        print("Cart delay. Waiting: " + str(cart_delay) + " seconds")
        time.sleep(float(cart_delay))
        add_to_cart = requests.post(cart_url, cookies=cookies)
        
        if combined_request == add_to_cart.text:
            cart = True
        else:
            cart = False
        return cart
    
    except Exception as e:
        print("Cart check failed:")
        print(e)
        cart = False
        return cart
    
def stock_check_func(request_data):
    for item in itertools.product (*request_data):
        data = {
            "kuni": "on", #this uses the english site and is required for cart check to work in a simple way
            "sir": item[0] + item[1],
            "size": item[2],
            "color": item[3]
        }
        try:
            utc_time_print = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
            stock_check = requests.post(request_url, data)
            stock_regex = re.search("^[0-z]+(?=\/)",stock_check.text)
            #in stock example: 4562332172443/FX-HI-XS-S-R/HIEN FX XSOFT S Wine red/2100.0/1/XSOFT/
            #out of stock example: NON/FX-HI-SF-XL-R/HIEN FX XSOFT S Wine red/2100.0/1/XSOFT/
            #out of stock example2: SELECT jan,model,sir,sir_eng,`in`,`out`,price,sale_price,kaigai_price,size,hardness FROM kai_price_local WHERE sir_id = 150 AND size = 3 AND color = 5
            
            #in stock
            if stock_regex == None or stock_regex.group(0) != "NON":
                cart = cart_check_func(stock_check.text)
                if cart == True:
                    stock_message = utc_time_print + ", Stock check: True, Cart check: True, Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
                    webhook_handler.webhook_sender(item)
                    print(stock_message)
                else:
                    stock_message = utc_time_print + ", Stock check: True, Cart check: False, Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
                    print(stock_message)
            #out of stock
            else:
                stock_message = utc_time_print + ", Stock check: False, Cart check: False, Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
                stock_state_tracker.find_item_state(item,"False")
                print(stock_message)
                
        except Exception as e:
            print("Stock check failed:")
            print(e)
            stock_message = utc_time_print + ", Stock check: Request failed, Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
            print(stock_message)
            print("Request fail delay. Waiting: " + str(request_fail_delay) + " seconds")
            time.sleep(float(request_fail_delay))
            
        try:
            with open ("artisan_stock_record_" + utc_time + ".txt", "a") as stock_record:
                stock_record.write(stock_message)
                stock_record.write("\n")
                
        except Exception as e:
            print("Could not open or write to file:")
            print(e)
        
        print("Stock delay. Waiting: " + str(stock_delay) + " seconds")
        time.sleep(float(stock_delay))

#verify that the webhook url is set and valid
webhook_handler.verify_webhook()

function_list = artisan_mousepads.active_functions()

while True:
    for element in function_list:
        stock_check_func(element())
    print("Batch delay. Waiting: " + str(batch_delay) + " seconds")
    time.sleep(float(batch_delay))
