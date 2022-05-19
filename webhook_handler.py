import re
import requests
import config_handler
import artisan_mousepads
import error_logger

def webhook_sender(item,stock_state,url):
    try:
        if stock_state == True:
            dict_mousepad_models = artisan_mousepads.mousepad_models()
            dict_hardnesses = artisan_mousepads.mousepad_hardnesses()
            dict_sizes = artisan_mousepads.mousepad_sizes()
            dict_colors = artisan_mousepads.mousepad_colors()
            dict_links = artisan_mousepads.mousepad_links()

            Model = dict_mousepad_models[item[0]]
            Hardness = dict_hardnesses[item[1]]
            Size = dict_sizes[item[2]]
            Color = dict_colors[item[3]]
            Link = dict_links[item[0]]
            
            content = config_handler.read("config.cfg","webhook","content")

            roles_dict = {
                "1" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Zero"),
                "11" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Hayate"),
                "12" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Hayate_Otsu"),
                "13" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Hayate_Kou"),
                "14" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Hien"),
                "15" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Hien_VE"),
                "16" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Zero"),
                "17" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Raiden"),
                "18" : config_handler.read("config.cfg","webhook_role_pings","role_FX_Shidenkai")
            }

            variable_dict = {
                "{Model}" : Model,
                "{Hardness}" : Hardness,
                "{Size}" : Size,
                "{Color}" : Color,
                "{Link}" : Link,
                "{Role Ping}" : roles_dict[item[0]]
            }

            for key in variable_dict.keys():
                content = re.sub(key, variable_dict[key], content)

            content = content.replace(r'\n', '\n')

            data = {
                "content" : content
            }
            
            requests.post(url,json=data)
    except Exception as e:
        print("!! SENDING WEBHOOK FAILED !!")
        error_logger.error_log("!! SENDING WEBHOOK FAILED !!",e)
    
def verify_webhook():
    try:
        url = config_handler.read("config.cfg","webhook","url")

        try:
            webhook_test = requests.get(url)
            if webhook_test.status_code != 200:
                print("Webhook URL not valid. Check that you put the correct URL in config.cfg.")
                print("Status code returned: " + str(webhook_test.status_code) + ". Expected 200")
                input()
            
            check_url = re.search("https://(canary\\.|ptb\\.|)discord(app)*\\.com/api/webhooks/\\d{18}/(\\w|-|_)*(/?)",url)
            if check_url == None:
                print("Webhook URL not valid. Check that you put the correct URL in config.cfg")
                print("Regex validation failed. If you believe this is incorrect, contact the devs or edit verify_webhook in webhook_handler.py")
                input()
            
        except Exception as e:
            error_logger.error_log("Webhook URL not valid. Check that you put the correct URL in config.cfg:",e)
            input()
        
    except Exception as e:
        error_logger.error_log("Webhook URL not found. Add the URL in config.cfg:",e)
        input()
    

