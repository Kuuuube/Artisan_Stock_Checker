from configparser import ConfigParser
import time
import hashlib
import traceback
import error_logger

def config_info(config_file):
    config = ConfigParser()
    config.read(config_file)
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
        "stock_delay": "30",
        "cart_delay": "30",
        "batch_delay": "0",
        "request_fail_delay": "120",
    }

    defaults["webhook"] = {
        "fallback_url": "",
        "S_url": "",
        "M_url": "",
        "L_url": "",
        "XL_url": "",
        "XXL_url": "",
        "content": "{Role Ping} In Stock!\\nModel: {Model}, Hardness: {Hardness}, Size: {Size}, Color: {Color}\\nLink: {Link}",
    }
    
    defaults["webhook_role_pings"] = {
        "role_CS_Zero": "<@&>",
        "role_CS_Raiden": "<@&>",
        "role_FX_Hayate_Otsu": "<@&>",
        "role_FX_Hayate_Kou": "<@&>",
        "role_FX_Hien": "<@&>",
        "role_FX_Zero": "<@&>",
        "role_FX_Raiden": "<@&>",
        "role_FX_Shidenkai": "<@&>",
        "role_FX_TYPE99": "<@&>",
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
            
        except Exception:
            if config_file == "config.cfg":
                error_logger.error_log("Config corrupted. Reverting to default:", traceback.format_exc())
                default_config(config_file)
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
            
        except Exception:
            if config_file == "config.cfg":
                error_logger.error_log("Config corrupted. Reverting to default:", traceback.format_exc())
                default_config(config_file)
            time.sleep(1)
