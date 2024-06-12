# Discord Webhook Script

## Dependencies

Python 3: [Download link](https://www.python.org/downloads/)

Python `requests` module: To install, enter the following command in cmd or a terminal:

```
pip install requests
```

## Usage

1. Run `./discord_webhook_script/check_artisan_stock_webhook.py` then close it to generate default settings file.

2. Open `config.cfg` and add your discord webhook url for `fallback_url = `. The fallback url is always required even if all size urls are present.

    Optional webhooks:

    Add multiple webhook urls to the different sizes (`s_url`, `m_url`, ...) to send to separate webhooks for pads of the specified size.

    Set `uptime_url` to receive notifications when the bot starts, a batch completes, or a critical error is hit.

3. Edit `content = ` to configure the message content you want to send when a mousepad goes from out of stock to in stock.

    `{Role Ping}` sends the content set for the pad specified under `[webhook_role_pings]`. 

    `{Model}` sends the mousepad model.

    `{Hardness}` sends the mousepad hardness.

    `{Size}` sends the mousepad size.

    `{Color}` sends the mousepad color.

    `{Link}` sends a link to the mousepad's store page.

4. Optionally, edit the delays in `config.cfg` to change the delay in seconds between checking stock, checking cart, looping batch, and request fail.

    `stock_delay` adds a delay after sending the stock check request.

    `cart_delay` adds a delay after sending the cart check request.

    `batch_delay` adds a delay between checking the full list of pads. Only used between the last item in the list and the first item in the list when looping back to the first item.

    `request_fail_delay` adds a delay after a request fails before resuming the sending of requests.

5. Run `./discord_webhook_script/check_artisan_stock_webhook.py`

## Removing stock checks

### To entirely remove stock checks for a mousepad:

Remove it from `function_list` in `./discord_webhook_script/artisan_mousepads.py`.

For example, to remove all FX Shidenkai stock checks:

Take this:

```python
function_list = [cs_zero,fx_hayate,fx_hayate_otsu,fx_hayate_kou,fx_hien,fx_hien_ve,fx_zero,fx_raiden,fx_shidenkai]
```

and remove `fx_shidenkai`:

```python
function_list = [cs_zero,fx_hayate,fx_hayate_otsu,fx_hayate_kou,fx_hien,fx_hien_ve,fx_zero,fx_raiden]
```

### To remove stock checks for specific hardnesses, sizes, or colors:

Remove them from their respective lists within the functions in `./discord_webhook_script/artisan_mousepads.py`. Check the dictionaries to find what each number checks for.

For example, to remove the XSoft check from the FX Shidenkai:

Take this:

```python
def fx_shidenkai():
    models = ["18"]
    hardnesses = ["0","2"]
    sizes = ["1","2","3","4"]
    colors = ["3","6","7"]
    return [models,hardnesses,sizes,colors]
```

and edit the `hardnesses` list:

```python
def fx_shidenkai():
    models = ["18"]
    hardnesses = ["2"]
    sizes = ["1","2","3","4"]
    colors = ["3","6","7"]
    return [models,hardnesses,sizes,colors]
```

To remove hardnesses from CS pads, remove the model number that includes the hardness. Check the `mousepad_hardnesses` function to find which model contains the hardness you need. Match the last digit of the model to the CS hardnesses section of the `mousepad_hardnesses` function.

For example, to remove the XSoft check from the CS Raiden:

Checking the CS section of the hardnesses list, we can see that under `CS Raiden`, XSoft is labeled `6` so the model ending in `6` is the one that needs to be removed.

```python
        #CS hardnesses are defined here
        hardness = model[-1]
        dict_hardnesses = {
            #CS Zero
            "3" : "XSoft",
            "4" : "Soft",
            "2" : "Mid",
            #CS Raiden
            "6" : "XSoft",
            "5" : "Mid"
        }
```

Take this:

```python
def cs_raiden():
    models = ["15","16"]
    hardnesses = [""]
    sizes = ["2","3","4"]
    colors = ["8"]
    return [models,hardnesses,sizes,colors]
```
and edit the `models` list:

```python
def cs_raiden():
    models = ["15"]
    hardnesses = [""]
    sizes = ["2","3","4"]
    colors = ["8"]
    return [models,hardnesses,sizes,colors]
```

## Adding stock checks

### Adding an entirely new pad

1. Find the model, hardnesses, sizes, and colors using your browser's developer/debug tools on the network tab. The data will be in the requests tab for `get_syouhin.php`. 

    The model will be the first two numbers after `sir`.

    The hardness will be the last number in `sir`. (For CS pads this will overlap with the model number.)

    The size will be the number in `size`.

    The color will be the number after `color`.

2. Add the model to the dictionary in `./discord_webhook_script/artisan_mousepads.py` along with hardnesses, sizes, and colors if those are not already accounted for. Make sure you add the pad in the correct section; do not mix the dictionaries for CS and FX pads. For example, adding a new mousepad model named `new_pad`:

    ```python
    dict_mousepad_models = {
        "11" : "FX Hayate",
        "12" : "FX Hayate Otsu",
        "13" : "FX Hayate Kou",
        "14" : "FX Hien",
        "15" : "FX Hien VE",
        "16" : "FX Zero",
        "17" : "FX Raiden",
        "18" : "FX Shidenkai",
        "19" : "New Pad"
    }
    ```

3. Make a new function for this new stock check in `./discord_webhook_script/artisan_mousepads.py`. For example, adding a function named `new_pad`:

    ```python
    def new_pad():
        models = ["19"]
        hardnesses = ["0","2"]
        sizes = ["1","2","3","4"]
        colors = ["3","6","7"]
        return [models,hardnesses,sizes,colors]
    ```

    For CS pads, model and hardness overlap. The hardnesses are handled as models. For example, adding a function named `cs_new_pad`:

    ```python
    def cs_new_pad():
        models = ["10","12"]
        hardnesses = [""]
        sizes = ["1","2","3","4"]
        colors = ["3","6","7"]
        return [models,hardnesses,sizes,colors]
    ```

4. Add this function to the functions list in `./discord_webhook_script/artisan_mousepads.py`. For example, adding the `new_pad` function to the list: 
    ```python
    function_list = [new_pad,cs_zero,fx_hayate,fx_hayate_otsu,fx_hayate_kou,fx_hien,fx_hien_ve,fx_zero,fx_raiden,fx_shidenkai]
    ```

5. Add the new pad to `roles_dict` in `./discord_webhook_script/webhook_handler.py` along with a new config file setting under `[webhook_role_pings]`. Adding it to the default config defined in `./discord_webhook_script/config_handler.py` may also be desirable but is not required.

### Adding new options to an existing pad

1. Find the new hardnesses, sizes, or colors using your browser's developer/debug tools on the network tab. The data will be in the requests tab for `get_syouhin.php`. 

    The hardness will be the last number in `sir`. (For CS pads the hardness and model are together so you will need to add a new model using both numbers in `sir` instead of adding a new hardness.)

    The size will be the number in `size`.

    The color will be the number after `color`.

2. Add the hardnesses, sizes, and colors to the dictionary if those are not already accounted for in `./discord_webhook_script/artisan_mousepads.py`. For example, adding color `9` as `New Color`:

    ```python
    dict_colors = {
    "1" : "Red",
    "2" : "Blue",
    "3" : "Black",
    "5" : "Black",
    "6" : "White",
    "7" : "Pink",
    "8" : "Brown",
    "9" : "New Color"
    }
    ```

3. Add the new hardnesses, sizes, or colors to the function in `./discord_webhook_script/artisan_mousepads.py`. For example, adding color `9` to the FX Raiden:

    ```python
    def fx_raiden():
    models = ["17"]
    hardnesses = ["0","2"]
    sizes = ["2","3","4"]
    colors = ["8","9"]
    return [models,hardnesses,sizes,colors]
    ```

    For CS pads only, hardnesses must be handled differently because the hardness will be attatched to the model. (Size and color are handled the same as FX) You will need to add a new model to the pad's function, a new entry to the CS hardnesses, models, links, and role pings dictionary. For example, adding a new hardness to the CS Raiden:

    Take this:

    ```python
    def cs_raiden():
    models = ["15","16"]
    hardnesses = [""]
    sizes = ["2","3","4"]
    colors = ["8"]
    return [models,hardnesses,sizes,colors]
    ```

    and edit the `models` list:

    ```python
    def cs_raiden():
    models = ["15","16","17"]
    hardnesses = [""]
    sizes = ["2","3","4"]
    colors = ["8"]
    return [models,hardnesses,sizes,colors]
    ```

    Now take the last digit in the new model and add it to the CS section of the `mousepad_hardnesses` dictionary:

    ```python
        #CS hardnesses are defined here
        hardness = model[-1]
        dict_hardnesses = {
            #CS Zero
            "3" : "XSoft",
            "4" : "Soft",
            "2" : "Mid",
            #CS Raiden
            "6" : "XSoft",
            "7" : "Soft",
            "5" : "Mid"
        }
    ```
    
    Take the model and add it to the CS section of the `mousepad_models` dictionary:

    ```python
        #CS models are defined here
        model = model + hardness
        dict_mousepad_models = {
            "12" : "CS Zero",
            "13" : "CS Zero",
            "14" : "CS Zero",
            "15" : "CS Raiden",
            "16" : "CS Raiden",
            "17" : "CS Raiden",
        }
    ```

    Take the model and add it to the CS section of the `mousepad_links` dictionary:

    ```python
        #CS models are defined here
        model = model + hardness
        dict_links = {
            "12" : "https://www.artisan-jp.com/cs-zero-eng.html",
            "13" : "https://www.artisan-jp.com/cs-zero-eng.html",
            "14" : "https://www.artisan-jp.com/cs-zero-eng.html",
            "15" : "https://artisan-jp.com/cs-raiden-eng.html",
            "16" : "https://artisan-jp.com/cs-raiden-eng.html"
            "17" : "https://artisan-jp.com/cs-raiden-eng.html"
        }
    ```

    Finally, in `./discord_webhook_script/webhook_handler.py` add the new model to `roles_dict`:

    ```python
        roles_dict = {
        "12" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Zero"),
        "13" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Zero"),
        "14" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Zero"),
        "15" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Raiden"),
        "16" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Raiden"),
        "17" : config_handler.read("config.cfg","webhook_role_pings","role_CS_Raiden"),
        }
    ```

## Troubleshooting

To reset settings to default, delete `config.cfg` and run the script. A new `config.cfg` will be generated with defaults.

To reset stock states and tracking, delete `stock_state.json`. This will remove the current stock data collected by the script. Upon running the script again it will rerecord the stock states. This will cause the script to resend webhook messages for items that had previously been recorded as in stock and have not had a change in state.