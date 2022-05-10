import requests
import re
import itertools
import time
from datetime import datetime,timezone

request_url = "https://www.artisan-jp.com/get_syouhin.php"
cart_url = "https://www.artisan-jp.com/stock_recheck.php"

#when adding a new mousepad model it must be added into the models dictionary
#new pads will likely fit existing hardness, size, and colors so those may not need to be edited
dict_mousepad_models = {
    "1" : "CS Zero",
    "11" : "FX Hayate",
    "12" : "FX Hayate Otsu",
    "13" : "FX Hayate Kou",
    "14" : "FX Hien",
    "15" : "FX Hien VE",
    "16" : "FX Zero",
    "17" : "FX Raiden",
    "18" : "FX Shidenkai"
}
dict_hardnesses = {
    "0" : "XSoft",
    "1" : "Soft",
    "2" : "Mid",
    "3" : "XSoft",
    "4" : "Soft"
}
dict_sizes = {
    "1" : "S",
    "2" : "M",
    "3" : "L",
    "4" : "XL"
}
dict_colors = {
    "1" : "Red",
    "2" : "Blue",
    "3" : "Black",
    "5" : "Black",
    "6" : "White",
    "7" : "Pink",
    "8" : "Brown"
}

utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

in_cart_list = []
only_stock_list = []
only_cart_list = []
cart = False

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
            
        #1 second delay to be polite
        time.sleep(1)

#functions for returning each pad's specifics
#refer to the dictionaries when editing these
def cs_zero():
    models = ["1"]
    hardnesses = ["3","4","2"]
    sizes = ["1","2","3","4"]
    colors = ["5"]
    return [models,hardnesses,sizes,colors]

def fx_hayate():
    models = ["11"]
    hardnesses = ["0","1","2"]
    sizes = ["2","3","4"]
    colors = ["5"]
    return [models,hardnesses,sizes,colors]

def fx_hayate_otsu():
    models = ["12"]
    hardnesses = ["0","1","2"]
    sizes = ["2","3","4"]
    colors = ["1","5"]
    return [models,hardnesses,sizes,colors]

def fx_hayate_kou():
    models = ["13"]
    hardnesses = ["0","1","2"]
    sizes = ["2","3","4"]
    colors = ["3"]
    return [models,hardnesses,sizes,colors]

def fx_hien():
    models = ["14"]
    hardnesses = ["0","1","2"]
    sizes = ["1","2","3","4"]
    colors = ["1","5"]
    return [models,hardnesses,sizes,colors]

def fx_hien_ve():
    models = ["15"]
    hardnesses = ["0"]
    sizes = ["1","2","3"]
    colors = ["1","2","5"]
    return [models,hardnesses,sizes,colors]

def fx_zero():
    models = ["16"]
    hardnesses = ["0","1","2"]
    sizes = ["1","2","3","4"]
    colors = ["5"]
    return [models,hardnesses,sizes,colors]

def fx_raiden():
    models = ["17"]
    hardnesses = ["0","2"]
    sizes = ["2","3","4"]
    colors = ["8"]
    return [models,hardnesses,sizes,colors]

def fx_shidenkai():
    models = ["18"]
    hardnesses = ["0","2"]
    sizes = ["1","2","3","4"]
    colors = ["3","6","7"]
    return [models,hardnesses,sizes,colors]

#list of all items to check stock for
#to skip checking items they can be removed from this list
function_list = [cs_zero,fx_hayate,fx_hayate_otsu,fx_hayate_kou,fx_hien,fx_hien_ve,fx_zero,fx_raiden,fx_shidenkai]

for element in function_list:
    stock_checker(element())

print("\n\n\nMousepads that are in stock and can be added to cart:")
for item in in_cart_list:
    print(item)
        
if len(in_cart_list) < 1:
    print("Nothing is in stock")

if len(only_stock_list) > 0:
    print("\n\n\nMousepads that are in stock and cannot be added to cart:")
    for item in only_stock_list:
        print(item)

input()
