import requests
import re
import itertools
import time
from datetime import datetime,timezone
import webhook_handler
import artisan_mousepads
import config_handler

request_url = "https://www.artisan-jp.com/get_syouhin.php"
cart_url = "https://www.artisan-jp.com/stock_recheck.php"

utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

in_cart_list = []
only_stock_list = []
cart = False
set_delay = config_handler.read("stock","delay")

dict_mousepad_models = artisan_mousepads.mousepad_models()
dict_hardnesses = artisan_mousepads.mousepad_hardnesses()
dict_sizes = artisan_mousepads.mousepad_sizes()
dict_colors = artisan_mousepads.mousepad_colors()

def check_cart(stock_check):
    try:
        split_request = stock_check.split("/")
        split_request[1] = split_request[1] + " " + split_request[2]
        split_request[2] = "1"
        del split_request[5]
        del split_request[5]
        combined_request = ",".join(split_request)
        
        cookies = {"cart":combined_request, "disc": "1", "lung": "jpf", "souryou": "800,SAL"}
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
    
def stock_checker(request_data):
    for item in itertools.product (*request_data):
        data = {
            "kuni": "on",
            "sir": item[0] + item[1],
            "size": item[2],
            "color": item[3]
        }
        try:
            stock_check = requests.post(request_url, data)
            stock_regex = re.search("^[0-z]+(?=\/)",stock_check.text)
            
            #in stock
            if stock_regex == None or stock_regex.group(0) != "NON":
                cart = check_cart(stock_check.text)
                if cart == True:
                    stock_message = "Stock check: True, Cart check: True, Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
                    in_cart_list.append(dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]])
                    webhook_handler.webhook_sender(item)
                    print(stock_message)
                else:
                    stock_message = "Stock check: True, Cart check: False, Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
                    only_stock_list.append(dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]])
                    print(stock_message)
            #out of stock
            else:
                stock_message = "Stock check: False, Cart check: False, Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
                print(stock_message)
                
        except Exception as e:
            print("Request failed:")
            print(e)
            stock_message = "Stock check: Request failed, Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
        try:
            with open ("artisan_stock_record_" + utc_time + ".txt", "a") as stock_record:
                stock_record.write(stock_message)
                stock_record.write("\n")
        except Exception as e:
            print("Could not open or write to file:")
            print(e)
            input()
            
        #15 second delay since this will constantly be looping
        time.sleep(int(set_delay))

function_list = artisan_mousepads.active_functions()

while True:
    for element in function_list:
        stock_checker(element())

    print("Mousepads that are in stock and can be added to cart:")
    for item in in_cart_list:
        print(item)
            
    if len(in_cart_list) < 1:
        print("Nothing is in stock")

    if len(only_stock_list) > 0:
        print("\n\n\nMousepads that are in stock and cannot be added to cart:")
        for item in only_stock_list:
            print(item)
