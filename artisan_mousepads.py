#when adding a new mousepad model it must be added into the models dictionary
#new pads will likely fit existing hardness, size, and colors so those may not need to be edited
def mousepad_models():
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
    return dict_mousepad_models

def mousepad_hardnesses():
    dict_hardnesses = {
        "0" : "XSoft",
        "1" : "Soft",
        "2" : "Mid",
        "3" : "XSoft",
        "4" : "Soft"
    }
    return dict_hardnesses

def mousepad_sizes():
    dict_sizes = {
        "1" : "S",
        "2" : "M",
        "3" : "L",
        "4" : "XL"
    }
    return dict_sizes

def mousepad_colors():
    dict_colors = {
        "1" : "Red",
        "2" : "Blue",
        "3" : "Black",
        "5" : "Black",
        "6" : "White",
        "7" : "Pink",
        "8" : "Brown"
    }
    return dict_colors

#uses the same numbers as mousepad_models to find links
def mousepad_links():
    dict_links = {
        "1" : "https://www.artisan-jp.com/cs-zero-eng.html",
        "11" : "https://www.artisan-jp.com/fx-hayate-eng.html",
        "12" : "https://www.artisan-jp.com/fx-hayate-otsu-eng.html",
        "13" : "https://www.artisan-jp.com/fx-hayate-kou-eng.html",
        "14" : "https://www.artisan-jp.com/fx-hien-eng.html",
        "15" : "https://www.artisan-jp.com/fx-hien-ve.html",
        "16" : "https://www.artisan-jp.com/fx-zero-eng.html",
        "17" : "https://www.artisan-jp.com/fx-raiden-eng.html",
        "18" : "https://www.artisan-jp.com/fx-shidenkai-eng.html"
        }
    return dict_links

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
def active_functions():
    function_list = [cs_zero,fx_hayate,fx_hayate_otsu,fx_hayate_kou,fx_hien,fx_hien_ve,fx_zero,fx_raiden,fx_shidenkai]
    return function_list
