# Basic Script

## Dependencies

Python 3: [Download link](https://www.python.org/downloads/)

Python `requests` module: To install, enter the following command in cmd or a terminal:

```
pip install requests
```

## Usage

1. Run `./basic_script/check_artisan_stock.py`

2. Optionally, edit the delays in `config.cfg` to change the delay in seconds between checking stock, checking cart, and request fail. (`config.cfg` is generated after starting the script once)

    `stock_delay` adds a delay after sending the stock check request.

    `cart_delay` adds a delay after sending the cart check request.

    `batch_delay` is unused in the basic script. It is for the webhook only.

    `request_fail_delay` adds a delay after a request fails before resuming the sending of requests.

## Removing stock checks (Optional)

### To entirely remove stock checks for a mousepad:

Remove it from `function_list` in `./basic_script/artisan_mousepads.py`.

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

Remove them from their respective lists within the functions in `./basic_script/artisan_mousepads.py`. Check the dictionaries to find what each number checks for.

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

## Adding stock checks (Optional)

### Adding an entirely new pad

1. Find the model, hardnesses, sizes, and colors using your browser's developer/debug tools on the network tab. The data will be in the requests tab for `get_syouhin.php`. 

    The model will be the first two numbers after `sir`.

    The hardness will be the last number in `sir`. (For CS pads this will overlap with the model number.)

    The size will be the number in `size`.

    The color will be the number after `color`.

2. Add the model to the dictionary in `./basic_script/artisan_mousepads.py` along with hardnesses, sizes, and colors if those are not already accounted for. Make sure you add the pad in the correct section; do not mix the dictionaries for CS and FX pads. For example, adding a new mousepad model named `new_pad`:

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

3. Make a new function for this new stock check in `./basic_script/artisan_mousepads.py`. For example, adding a function named `new_pad`:

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

4. Add this function to the functions list in `./basic_script/artisan_mousepads.py`. For example, adding the `new_pad` function to the list: 
    ```python
    function_list = [new_pad,cs_zero,fx_hayate,fx_hayate_otsu,fx_hayate_kou,fx_hien,fx_hien_ve,fx_zero,fx_raiden,fx_shidenkai]
    ```

### Adding new options to an existing pad

1. Find the new hardnesses, sizes, or colors using your browser's developer/debug tools on the network tab. The data will be in the requests tab for `get_syouhin.php`. 

    The hardness will be the last number in `sir`. (For CS pads the hardness and model are together so you will need to add a new model using both numbers in `sir` instead of adding a new hardness.)

    The size will be the number in `size`.

    The color will be the number after `color`.

2. Add the hardnesses, sizes, and colors to the dictionary if those are not already accounted for in `./basic_script/artisan_mousepads.py`. For example, adding color `9` as `New Color`:

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

3. Add the new hardnesses, sizes, or colors to the function in `./basic_script/artisan_mousepads.py`. For example, adding color `9` to the FX Raiden:

    ```python
    def fx_raiden():
    models = ["17"]
    hardnesses = ["0","2"]
    sizes = ["2","3","4"]
    colors = ["8","9"]
    return [models,hardnesses,sizes,colors]
    ```

    For CS pads only, hardnesses must be handled differently because the hardness will be attatched to the model. (Size and color are handled the same as FX) You will need to add a new model to the pad's function, a new entry to the CS hardnesses dictionary, and a new entry to the CS models dictionary. For example, adding a new hardness to the CS Raiden:

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
    
    Finally, take the model and add it to the CS section of the `mousepad_models` dictionary:

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

## Troubleshooting

To reset settings to default, delete `config.cfg` and run the script. A new `config.cfg` will be generated with defaults.