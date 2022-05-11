from configparser import ConfigParser
import sys
import time

config_file = "config.cfg"

def config_info():
    config = ConfigParser()
    config.read(config_file)
    config.sections()
    return config

def default_config():
    defaults = ConfigParser()
    defaults["stock"] = {
    "delay": "1",
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

def read(section,name):
    function_success = False
    while function_success == False:
        try:
            config = config_info()
            return config.get(section,name)
            function_success == True
        except Exception as e:
            print(e)
            print("Config corrupted. Reverting to default.")
            default_config()
            time.sleep(1)

def write(section,name,value):
    function_success = False
    while function_success == False:
        try:
            config = config_info()
            config[section][name] = value
            with open(config_file, 'w') as conf:
                config.write(conf)
            function_success = True
        except Exception as e:
            print(e)
            print("Config corrupted. Reverting to default.")
            default_config()
            time.sleep(1)
