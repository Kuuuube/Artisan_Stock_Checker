import requests
import re
import itertools
import time
from datetime import datetime,timezone
import webhook_handler
import artisan_mousepads
import config_handler
import stock_state_tracker
import stock_checker

utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

dict_mousepad_models = artisan_mousepads.mousepad_models()
dict_hardnesses = artisan_mousepads.mousepad_hardnesses()
dict_sizes = artisan_mousepads.mousepad_sizes()
dict_colors = artisan_mousepads.mousepad_colors()

stock_delay = config_handler.read("config.cfg","stock","stock_delay")
cart_delay = config_handler.read("config.cfg","stock","cart_delay")
batch_delay = config_handler.read("config.cfg","stock","batch_delay")
request_fail_delay = config_handler.read("config.cfg","stock","request_fail_delay")

def stock_check_runner(request_data):
    cart_info = "False"
    
    for item in itertools.product (*request_data):
        stock_info = stock_checker.stock_check_func(item)
        print("Stock delay. Waiting: " + str(stock_delay) + " seconds")
        time.sleep(float(stock_delay))
        
        if stock_info[0] == "True":
            cart_info = stock_checker.cart_check_func(stock_info[1])
            
            if cart_info == "True":
                stock_state = stock_state_tracker.find_item_state(item,"True")
                webhook_handler.webhook_sender(item,stock_state)
                
            else:
                stock_state_tracker.find_item_state(item,"False")

            #cart delay here to allow webhook to send without this delay before it
            print("Cart delay. Waiting: " + str(cart_delay) + " seconds")
            time.sleep(float(cart_delay))
            
        elif stock_info[0] == "Request failed":
            print("Request fail delay. Waiting: " + str(request_fail_delay) + " seconds")
            time.sleep(float(request_fail_delay))
            
        else:
            stock_state_tracker.find_item_state(item,"False")

        utc_time_print = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        stock_message = utc_time_print + ", Stock check: " + str(stock_info[0]) + ", Cart check: " + cart_info + ", Model: " + dict_mousepad_models[item[0]] + ", Hardness: " + dict_hardnesses[item[1]] + ", Size: " + dict_sizes[item[2]] + ", Color: " + dict_colors[item[3]]
        print(stock_message)

    try:
        with open ("artisan_stock_record_" + utc_time + ".txt", "a") as stock_record:
                stock_record.write(stock_message)
                stock_record.write("\n")
                
    except Exception as e:
        print("Could not open or write to file:")
        print(e)

        
#verify that the webhook url is set and valid
webhook_handler.verify_webhook()

function_list = artisan_mousepads.active_functions()

while True:
    for element in function_list:
        stock_check_runner(element())
    print("Batch delay. Waiting: " + str(batch_delay) + " seconds")
    time.sleep(float(batch_delay))
