from configparser import ConfigParser
import sys
import time
import hashlib

def config_info(config_file):
    config = ConfigParser()
    config.read(config_file)
    config.sections()
    return config

def backup_bad_config(config_file):
    try:
        with open(config_file,"rb") as hashfile:
            bytes = hashfile.read()
            hash_value = hashlib.md5(bytes).hexdigest();
        with open(config_file, 'r') as conf, open(config_file + ".bak" + hash_value, "w") as backup:
            for line in conf:
                backup.write(line)
    except Exception:
        pass

def default_config(config_file):
    backup_bad_config(config_file)
    
    defaults = ConfigParser()
    defaults["stock"] = {
        "delay": "5",
    }

    defaults["webhook"] = {
        "url": "",
        "content": "{Role Ping} In Stock! Model: {Model}, Hardness: {Hardness}, Size: {Size}, Color: {Color}, Link: {Link}",
    }
    
    defaults["webhook_role_pings"] = {
        "role_CS_Zero": "<@&>",
        "role_FX_Hayate": "<@&>",
        "role_FX_Hayate_Otsu": "<@&>",
        "role_FX_Hayate_Kou": "<@&>",
        "role_FX_Hien": "<@&>",
        "role_FX_Hien_VE": "<@&>",
        "role_FX_Zero": "<@&>",
        "role_FX_Raiden": "<@&>",
        "role_FX_Shidenkai": "<@&>",
    }
    
    with open(config_file, 'w') as conf:
        defaults.write(conf)

def default_stock_state(config_file):
    backup_bad_config(config_file)
        
    defaults = ConfigParser()
    defaults["modelhardnesssizecolor"] = {
        "1315": "False",
        "1325": "False",
        "1335": "False",
        "1345": "False",
        "1415": "False",
        "1425": "False",
        "1435": "False",
        "1445": "False",
        "1215": "False",
        "1225": "False",
        "1235": "False",
        "1245": "False",
        "11025": "False",
        "11035": "False",
        "11045": "False",
        "11125": "False",
        "11135": "False",
        "11145": "False",
        "11225": "False",
        "11235": "False",
        "11245": "False",
        "12021": "False",
        "12025": "False",
        "12031": "False",
        "12035": "False",
        "12041": "False",
        "12045": "False",
        "12121": "False",
        "12125": "False",
        "12131": "False",
        "12135": "False",
        "12141": "False",
        "12145": "False",
        "12221": "False",
        "12225": "False",
        "12231": "False",
        "12235": "False",
        "12241": "False",
        "12245": "False",
        "13023": "False",
        "13033": "False",
        "13043": "False",
        "13123": "False",
        "13133": "False",
        "13143": "False",
        "13223": "False",
        "13233": "False",
        "13243": "False",
        "14011": "False",
        "14015": "False",
        "14021": "False",
        "14025": "False",
        "14031": "False",
        "14035": "False",
        "14041": "False",
        "14045": "False",
        "14111": "False",
        "14115": "False",
        "14121": "False",
        "14125": "False",
        "14131": "False",
        "14135": "False",
        "14141": "False",
        "14145": "False",
        "14211": "False",
        "14215": "False",
        "14221": "False",
        "14225": "False",
        "14231": "False",
        "14235": "False",
        "14241": "False",
        "14245": "False",
        "15011": "False",
        "15012": "False",
        "15015": "False",
        "15021": "False",
        "15022": "False",
        "15025": "False",
        "15031": "False",
        "15032": "False",
        "15035": "False",
        "16015": "False",
        "16025": "False",
        "16035": "False",
        "16045": "False",
        "16115": "False",
        "16125": "False",
        "16135": "False",
        "16145": "False",
        "16215": "False",
        "16225": "False",
        "16235": "False",
        "16245": "False",
        "17028": "False",
        "17038": "False",
        "17048": "False",
        "17228": "False",
        "17238": "False",
        "17248": "False",
        "18013": "False",
        "18016": "False",
        "18017": "False",
        "18023": "False",
        "18026": "False",
        "18027": "False",
        "18033": "False",
        "18036": "False",
        "18037": "False",
        "18043": "False",
        "18046": "False",
        "18047": "False",
        "18213": "False",
        "18216": "False",
        "18217": "False",
        "18223": "False",
        "18226": "False",
        "18227": "False",
        "18233": "False",
        "18236": "False",
        "18237": "False",
        "18243": "False",
        "18246": "False",
        "18247": "False",
    }
    
    with open(config_file, 'w') as conf:
        defaults.write(conf)

def read(config_file,section,name):
    function_success = False
    while function_success == False:
        try:
            config = config_info(config_file)
            return config.get(section,name)
            function_success == True
        except Exception as e:
            print(e)
            print("Config corrupted. Reverting to default.")
            if config_file == "config.cfg":
                default_config(config_file)
            if config_file == "stock_state.cfg":
                default_stock_state(config_file)
            time.sleep(1)

def read_section(config_file,section):
    function_success = False
    section_list = []
    while function_success == False:
        try:
            config = config_info(config_file)
            for item in config[section]:
                section_list.append(item)
            return section_list
            function_success == True
        except Exception as e:
            print(e)
            print("Config or Stock State corrupted. Reverting to default.")
            if config_file == "config.cfg":
                print("Config corrupted. Reverting to default.")
                default_config(config_file)
            if config_file == "stock_state.cfg":
                print("Stock state corrupted. Reverting to default.")
                default_stock_state(config_file)
            time.sleep(1)

def write(config_file,section,name,value):
    function_success = False
    while function_success == False:
        try:
            config = config_info(config_file)
            config[section][name] = value
            with open(config_file, 'w') as conf:
                config.write(conf)
            function_success = True
        except Exception as e:
            print(e)
            if config_file == "config.cfg":
                print("Config corrupted. Reverting to default.")
                default_config(config_file)
            if config_file == "stock_state.cfg":
                print("Stock state corrupted. Reverting to default.")
                default_stock_state(config_file)
            time.sleep(1)
