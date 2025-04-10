# when adding a new mousepad model it must be added into the models dictionary
# new pads will likely fit existing hardness, size, and colors so those may not need to be edited
def mousepad_models(model, hardness):
    if len(hardness) == 1 and int(hardness) <= 2:
        # FX models are defined here
        dict_mousepad_models = {
            "11": "FX Hayate",
            "12": "FX Hayate Otsu",
            "13": "FX Hayate Kou",
            "14": "FX Hien",
            "15": "FX Hien VE",
            "16": "FX Zero",
            "17": "FX Raiden",
            "18": "FX Shidenkai",
            "19": "FX Shidenkai",
            "21": "FX TYPE-99",
            "22": "FX KEY83",
        }
    elif len(hardness) == 1 and int(hardness) > 2:
        dict_mousepad_models = {
            "22": "FX Hayate Otsu V2",
        }
    else:
        # CS models and skates are defined here
        model = model + hardness
        dict_mousepad_models = {
            "12": "CS Zero",
            "13": "CS Zero",
            "14": "CS Zero",
            "15": "CS Raiden",
            "16": "CS Raiden",
            "1000": "Mizugumo Futae P8",
        }
    return dict_mousepad_models[model]


def mousepad_hardnesses(model, hardness):
    if len(hardness) == 1:
        # FX hardnesses are defined here
        # Most pads are hardness 0-2, FX Hayate Otsu v2 is weird and takes up 3-5
        dict_hardnesses = {"0": "XSoft", "1": "Soft", "2": "Mid", "3": "XSoft", "4": "Soft", "5": "Mid"}
    else:
        # CS hardnesses are defined here
        hardness = model[-1]
        dict_hardnesses = {
            # CS Zero
            "3": "XSoft",
            "4": "Soft",
            "2": "Mid",
            # CS Raiden
            "6": "XSoft",
            "5": "Mid",
        }
    if hardness not in dict_hardnesses:
        return "N/A"
    return dict_hardnesses[hardness]


def mousepad_sizes(model, hardness, size):
    if len(model + hardness) == 4:
        return "N/A"
    dict_sizes = {"1": "S", "2": "M", "3": "L", "4": "XL", "5": "XXL"}
    return dict_sizes[size]


def mousepad_colors(colors):
    dict_colors = {
        "1": "Red",
        "2": "Blue",
        "3": "Black",
        "5": "Black",
        "6": "White",
        "7": "Pink",
        "8": "Brown",
        "10": "Orange",
        "11": "Black",
        "12": "Matcha",
        "13": "Gray",
    }
    if colors not in dict_colors:
        return "N/A"
    return dict_colors[colors]


# uses the same numbers as mousepad_models to find links
def mousepad_links(model, hardness):
    if len(hardness) == 1 and int(hardness) <= 2:
        # FX links are defined here
        dict_links = {
            "1": "https://www.artisan-jp.com/cs-zero-eng.html",
            "11": "https://www.artisan-jp.com/fx-hayate-eng.html",
            "12": "https://www.artisan-jp.com/fx-hayate-otsu-eng.html",
            "13": "https://www.artisan-jp.com/fx-hayate-kou-eng.html",
            "14": "https://www.artisan-jp.com/fx-hien-eng.html",
            "15": "https://www.artisan-jp.com/fx-hien-ve.html",
            "16": "https://www.artisan-jp.com/fx-zero-eng.html",
            "17": "https://www.artisan-jp.com/fx-raiden-eng.html",
            "18": "https://www.artisan-jp.com/fx-shidenkai-eng.html",
            "19": "https://www.artisan-jp.com/fx-shidenkai-eng.html",
            "21": "https://www.artisan-jp.com/fx-99-eng.html",
            "22": "https://www.artisan-jp.com/fx-k83-eng.html",
        }
    elif len(hardness) == 1 and int(hardness) > 2:
        dict_links = {
            "22": "https://artisan-jp.com/fx-hayate-otsu-v2-eng.html",
        }
    else:
        # CS models are defined here
        model = model + hardness
        dict_links = {
            "12": "https://www.artisan-jp.com/cs-zero-eng.html",
            "13": "https://www.artisan-jp.com/cs-zero-eng.html",
            "14": "https://www.artisan-jp.com/cs-zero-eng.html",
            "15": "https://www.artisan-jp.com/cs-raiden-eng.html",
            "16": "https://www.artisan-jp.com/cs-raiden-eng.html",
            "1000": "https://artisan-jp.com/fx-sole305_eng.html",
        }
    return dict_links[model]


# functions for returning each pad's specifics
# refer to the dictionaries when editing these
def cs_zero():
    models = ["13", "14", "12"]
    hardnesses = [""]
    sizes = ["1", "2", "3", "4"]
    colors = ["5"]
    return [models, hardnesses, sizes, colors]


def cs_raiden():
    models = ["15", "16"]
    hardnesses = [""]
    sizes = ["2", "3", "4"]
    colors = ["8"]
    return [models, hardnesses, sizes, colors]


def fx_hayate_otsu():
    models = ["12"]
    hardnesses = ["0", "1", "2"]
    sizes = ["2", "3", "4", "5"]
    colors = ["1", "5"]
    return [models, hardnesses, sizes, colors]


def fx_hayate_otsu_v2():
    models = ["22"]
    hardnesses = ["3", "4", "5"]
    sizes = ["2", "3", "4", "5"]
    colors = ["1", "5"]
    return [models, hardnesses, sizes, colors]


def fx_hayate_kou():
    models = ["13"]
    hardnesses = ["0", "1", "2"]
    sizes = ["2", "3", "4", "5"]
    colors = ["3"]
    return [models, hardnesses, sizes, colors]


def fx_hien():
    models = ["14"]
    hardnesses = ["0", "1", "2"]
    sizes = ["1", "2", "3", "4", "5"]
    colors = ["1", "5"]
    return [models, hardnesses, sizes, colors]


def fx_zero():
    models = ["16"]
    hardnesses = ["0", "1", "2"]
    sizes = ["1", "2", "3", "4", "5"]
    colors = ["5", "10"]
    return [models, hardnesses, sizes, colors]


def fx_raiden():
    models = ["17"]
    hardnesses = ["0", "1", "2"]
    sizes = ["2", "3", "4", "5"]
    colors = ["8", "10"]
    return [models, hardnesses, sizes, colors]


def fx_shidenkai():
    models = ["19"]
    hardnesses = ["0", "2"]
    sizes = ["3", "4"]
    colors = ["6", "10", "11"]
    return [models, hardnesses, sizes, colors]


def fx_type99():
    models = ["21"]
    hardnesses = ["0", "1", "2"]
    sizes = ["3", "4", "5"]
    colors = ["5", "12", "13"]
    return [models, hardnesses, sizes, colors]


def fx_key83():
    models = ["22"]
    hardnesses = ["0", "1", "2"]
    sizes = ["2", "3", "4", "5"]
    colors = ["5"]
    return [models, hardnesses, sizes, colors]


def skates():
    models = ["10"]
    hardnesses = ["00"]
    sizes = ["1"]
    colors = ["0"]
    return [models, hardnesses, sizes, colors]


# list of all items to check stock for
# to skip checking items they can be removed from this list
def active_functions():
    function_list = [
        cs_zero,
        cs_raiden,
        fx_hayate_otsu,
        fx_hayate_otsu_v2,
        fx_hayate_kou,
        fx_hien,
        fx_zero,
        fx_raiden,
        fx_shidenkai,
        fx_type99,
        fx_key83,
        skates,
    ]
    return function_list
