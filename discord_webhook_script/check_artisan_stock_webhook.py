import itertools
import time
from datetime import datetime,timezone
import webhook_handler
import artisan_mousepads
import config_handler
import stock_state_tracker
import stock_checker
import error_logger

utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

stock_delay = config_handler.read("config.cfg","stock","stock_delay")
cart_delay = config_handler.read("config.cfg","stock","cart_delay")
batch_delay = config_handler.read("config.cfg","stock","batch_delay")
request_fail_delay = config_handler.read("config.cfg","stock","request_fail_delay")

#verify that the webhook fallback_url is set and valid
webhook_handler.verify_webhook()

#define the fallback_url here for extra stability incase the config gets reset
fallback_url = config_handler.read("config.cfg","webhook","fallback_url")

def stock_check_runner(request_data):
    for item in itertools.product (*request_data):
        cart_info = "False"
        stock_info = stock_checker.stock_check_func(item)
        print("Stock delay. Waiting: " + str(stock_delay) + " seconds")
        time.sleep(float(stock_delay))
        
        if stock_info[0] == "True":
            cart_info = stock_checker.cart_check_func(stock_info[1])
            
            if cart_info == "True":
                stock_state = stock_state_tracker.find_item_state(item,"True")
                webhook_handler.webhook_sender(item,stock_state,fallback_url)
                
            elif cart_info == "False":
                stock_state_tracker.find_item_state(item,"False")

            #cart delay here to allow webhook to send without this delay before it
            print("Cart delay. Waiting: " + str(cart_delay) + " seconds")
            time.sleep(float(cart_delay))

        elif stock_info[0] == "False":
            stock_state_tracker.find_item_state(item,"False")

        #this must use if not elif since cart_info will never be checked otherwise
        if stock_info[0] == "Request failed" or cart_info == "Request failed":
            print("Request fail delay. Waiting: " + str(request_fail_delay) + " seconds")
            time.sleep(float(request_fail_delay))
            
        utc_time_print = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        stock_message = utc_time_print + ", Stock check: " + str(stock_info[0]) + ", Cart check: " + cart_info + ", Model: " + artisan_mousepads.mousepad_models(item[0],item[1]) + ", Hardness: " + artisan_mousepads.mousepad_hardnesses(item[0],item[1]) + ", Size: " + artisan_mousepads.mousepad_sizes(item[2]) + ", Color: " + artisan_mousepads.mousepad_colors(item[3])
        print(stock_message)

        try:
            with open ("artisan_stock_record_" + utc_time + ".txt", "a") as stock_record:
                    stock_record.write(stock_message)
                    stock_record.write("\n")
                    
        except Exception as e:
            error_logger.error_log("Could not open or write to file:",e)


try:
    function_list = artisan_mousepads.active_functions()
except Exception as e:
    error_logger.error_log("Functions list not set properly:",e)
    input()

while True:
    try:
        for element in function_list:
            stock_check_runner(element())
        print("Batch delay. Waiting: " + str(batch_delay) + " seconds")
        time.sleep(float(batch_delay))
    except Exception as e:
        error_logger.error_log("Critical failure in stock_check_runner:",e)
