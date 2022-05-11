from discord import Webhook, RequestsWebhookAdapter
import re
import config_handler
import artisan_mousepads

def webhook_sender(item):
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
    
    url = config_handler.read("config.cfg","webhook","url")
    
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
    
    webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
    webhook.send(content=content)
