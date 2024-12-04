import re
import requests
import traceback
import config_handler
import artisan_mousepads
import error_logger

def roles_dict(model,hardness):
    try:
        if len(hardness) == 1:
            #FX models are defined here
            roles_dict = {
                "12" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Hayate_Otsu"),
                "13" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Hayate_Kou"),
                "14" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Hien"),
                "16" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Zero"),
                "17" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Raiden"),
                "18" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Shidenkai"),
                "19" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Shidenkai"),
                "21" : config_handler.read("config.cfg","webhook_role_pings","role_FX_TYPE99"),
                "22" : config_handler.read("config.cfg","webhook_role_pings","role_FX_KEY83")
            }
        else:
            #CS models are defined here
            model = model + hardness
            roles_dict = {
                "12" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Zero"),
                "13" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Zero"),
                "14" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Zero"),
                "15" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Raiden"),
                "16" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Raiden")
            }
            
        return roles_dict[model]
    except Exception:
        error_logger.error_log("Could not read role pings in config", traceback.format_exc())
        return "Invalid role ping"

def get_webhook_url(size,fallback_url):
    match size:
        case "S":
            return config_handler.read("config.cfg","webhook","s_url")
        case "M":
            return config_handler.read("config.cfg","webhook","m_url")
        case "L":
            return config_handler.read("config.cfg","webhook","l_url")
        case "XL":
            return config_handler.read("config.cfg","webhook","xl_url")
        case "XXL":
            return config_handler.read("config.cfg","webhook","xxl_url")
        case _:
            return fallback_url

def webhook_sender(item, stock_state, fallback_url, request_fail_delay = 240):
    try:
        if stock_state == True:

            Model = artisan_mousepads.mousepad_models(item[0],item[1])
            Hardness = artisan_mousepads.mousepad_hardnesses(item[0],item[1])
            Size = artisan_mousepads.mousepad_sizes(item[2])
            Color = artisan_mousepads.mousepad_colors(item[3])
            Link = artisan_mousepads.mousepad_links(item[0],item[1])
            
            content = config_handler.read("config.cfg","webhook","content")

            variable_dict = {
                "{Model}" : Model,
                "{Hardness}" : Hardness,
                "{Size}" : Size,
                "{Color}" : Color,
                "{Link}" : Link,
                "{Role Ping}" : roles_dict(item[0],item[1])
            }
            
            for key in variable_dict.keys():
                content = re.sub(key, variable_dict[key], content)

            content = content.replace(r'\n', '\n')

            data = {
                "content" : content
            }

            url = get_webhook_url(Size,fallback_url)
            if not url:
                url = fallback_url
            
            requests.post(url,json=data, timeout=request_fail_delay)
    except Exception:
        print("!! SENDING WEBHOOK FAILED !!")
        error_logger.error_log("!! SENDING WEBHOOK FAILED !!", traceback.format_exc())
    
def verify_webhook(request_fail_delay = 240):
    try:
        url = config_handler.read("config.cfg","webhook","fallback_url")

        try:
            webhook_test = requests.get(url, timeout=request_fail_delay)
            if webhook_test.status_code != 200:
                print("Webhook URL not valid. Check that you put the correct URL in config.cfg.")
                print("Status code returned: " + str(webhook_test.status_code) + ". Expected 200")
                input()
            
            check_url = re.search("https://(canary\\.|ptb\\.|)discord(app)*\\.com/api/webhooks/\\d+/(\\w|-|_)*(/?)",url)
            if check_url == None:
                print("Webhook URL not valid. Check that you put the correct URL in config.cfg")
                print("Regex validation failed. If you believe this is incorrect, contact the devs or edit verify_webhook in webhook_handler.py")
                input()
            
        except Exception:
            error_logger.error_log("Webhook URL not valid. Check that you put the correct URL in config.cfg:", traceback.format_exc())
            input()
        
    except Exception:
        error_logger.error_log("Webhook URL not found. Add the URL in config.cfg:", traceback.format_exc())
        input()
    
def send_uptime_webhook(data, request_fail_delay = 240):
    try:
        url = config_handler.read("config.cfg","webhook","uptime_url")
        requests.post(url = url, json = data, timeout=request_fail_delay)
    except Exception:
        error_logger.error_log("Uptime webhook failed", traceback.format_exc())
