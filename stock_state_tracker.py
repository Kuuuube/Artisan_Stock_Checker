import config_handler

def find_item_state(item,stock_state):
    mousepad_list = config_handler.read_section("stock_state.cfg","modelhardnesssizecolor")
    mousepad_list_combined = "".join(item)
    
    for element in mousepad_list:
        if element == mousepad_list_combined:
            if stock_state == config_handler.read("stock_state.cfg","modelhardnesssizecolor",mousepad_list_combined):
                return False
            else:
                config_handler.write("stock_state.cfg","modelhardnesssizecolor",mousepad_list_combined,stock_state)
                return True
