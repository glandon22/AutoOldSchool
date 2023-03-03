import datetime

from osrs_utils import general_utils, keyboard

port = '56799'

start_point_diff = {
    'x': 4,
    'y': -12
}

modified_start_point_diff = {
    'x': 5,
    'y': -12
}

row_5_point_diff = {
    'x': 10,
    'y': -1
}

deposit_sack = {
    'x': 1,
    'y': 1
}

def start_game():
    table = general_utils.get_game_object('1803,3504,0', '27430', port)
    general_utils.move_and_click(table['x'], table['y'], 3, 3)
    while True:
        seeds = general_utils.get_chat_options(port)
        if seeds:
            opt = general_utils.select_chat_option(seeds, 'Golovanova')
            keyboard.type(str(opt))
            general_utils.random_sleep(0.5, 0.6)
            break
    general_utils.random_sleep(1, 1.1)
    door = general_utils.get_wall_object('1805,3501,0', '27445', port)
    general_utils.move_and_click(door['x'], door['y'], 3, 3)
    general_utils.random_sleep(3, 3.1)
    inv = general_utils.get_inv(port, True)
    fert = general_utils.is_item_in_inventory_v2(inv, '13420')
    general_utils.right_click_menu_select(fert, None, port, 'Gricoller\'s fertiliser', 'Drop')

# in prog
def leave_game():
    door = general_utils.get_surrounding_wall_objects(7, ['27445'], port)
    print(door)
    if '27445' in door:
        general_utils.move_and_click(door['27445'][0]['x'], door['27445'][0]['y'], 2, 2)
    general_utils.random_sleep(3, 3.1)

def fill_watering_cans():
    while True:
        inv = general_utils.get_inv(port)
        not_full_can = general_utils.are_items_in_inventory_v2(inv, [5331, 5333, 5334, 5335, 5336, 5337, 5338, 5339])
        if not_full_can:
            general_utils.move_and_click(not_full_can['x'], not_full_can['y'], 3, 3)
            water = general_utils.get_surrounding_game_objects(10, ['5598'], port)
            if '5598' in water:
                general_utils.move_and_click(water['5598']['x'], water['5598']['y'], 2, 2)
                general_utils.random_sleep(0.6, 0.7)
        else:
            break


def deposit_fruit():
    while True:
        inv = general_utils.get_inv(port)
        sack = general_utils.get_surrounding_game_objects(5, ['27431'], port)
        if '27431' in sack:
            general_utils.move_and_click(sack['27431']['x'], sack['27431']['y'], 2, 2)
            general_utils.random_sleep(0.6, 0.7)
            while True:
                if inv != general_utils.get_inv(port, True):
                    return


def get_in_position_v2(anchor, diff):
    general_utils.run_towards_square({'x': anchor['x_coord'] + diff['x'], 'y': anchor['y_coord'] + diff['y'], 'z': 0}, port)

def get_in_position():
    loc = general_utils.get_world_location(port)
    general_utils.run_towards_square({'x': loc['x'] + 5, 'y': loc['y'] - 12, 'z': 0}, port)

def run_to_fifth_row():
    loc = general_utils.get_world_location(port)
    general_utils.run_towards_square({'x': loc['x'] + 6, 'y': loc['y'] - 12, 'z': 0}, port)


def plant_seed(amount):
    planted = 0
    while planted < amount:
        inv = general_utils.get_inv(port)
        seed = general_utils.is_item_in_inventory_v2(inv, '13423')
        starting_seed_quant = seed['quantity']
        general_utils.move_and_click(seed['x'], seed['y'], 3, 3)
        patches = general_utils.get_multiple_surrounding_game_objects(10, ['27383'], port)
        closest = general_utils.find_closest_target(patches['27383'])
        general_utils.move_and_click(closest['x'], closest['y'], 2, 2)
        while True:
            inv = general_utils.get_inv(port, True)
            seed = general_utils.is_item_in_inventory_v2(inv, '13423')
            if not seed or seed['quantity'] != starting_seed_quant:
                break
        watering_can = general_utils.are_items_in_inventory_v2(inv, [5340, 5333, 5334, 5335, 5336, 5337, 5338, 5339])
        general_utils.move_and_click(watering_can['x'], watering_can['y'], 3, 3)
        patches = general_utils.get_multiple_surrounding_game_objects(2, ['27384'], port)
        closest = general_utils.find_closest_target(patches['27384'])
        general_utils.move_and_click(closest['x'], closest['y'], 2, 2)
        general_utils.random_sleep(0.6, 0.7)
        planted += 1

def water_plant(amount, obj_id):
    planted = 0
    while planted < amount:
        inv = general_utils.get_inv(port)
        blighted = False
        while True:
            patches = general_utils.get_multiple_surrounding_game_objects(10, [obj_id, 27386, 27389, 27392], port)
            possible_objs = []
            if bool(patches):
                if obj_id in patches:
                    possible_objs = patches[obj_id] + possible_objs
                if '27386' in patches:
                    blighted = True
                    possible_objs = patches['27386'] + possible_objs
                if '27389' in patches:
                    blighted = True
                    possible_objs = patches['27389'] + possible_objs
                if '27392' in patches:
                    blighted = True
                    possible_objs = patches['27392'] + possible_objs
                closest = general_utils.find_closest_target(possible_objs)
                general_utils.move_and_click(closest['x'], closest['y'], 2, 2)
                break
        start = datetime.datetime.now()
        while True:
            curr_inv = general_utils.get_inv(port)
            if inv != curr_inv or blighted or (datetime.datetime.now() - start).total_seconds() > 9:
                break
        general_utils.random_sleep(0.7, 0.8)
        planted += 1

def determine_anchor_tile():
    while True:
        water = general_utils.get_surrounding_game_objects(10, ['5598'], port)
        if '5598' in water:
            return water['5598']


def drink_stam():
    run_energy = general_utils.get_widget('160,28', port)
    if run_energy and int(run_energy['text']) < 35:
        inv = general_utils.get_inv(port, True)
        stam = general_utils.are_items_in_inventory_v2(inv, [12631, 12629, 12627, 12625])
        if stam:
            general_utils.move_and_click(stam['x'], stam['y'], 3, 3)
            general_utils.random_sleep(1, 1.1)

def main():
    start_game()
    anchor = determine_anchor_tile()
    iters_14 = 0
    while iters_14 < 5:
        fill_watering_cans()
        get_in_position_v2(anchor, start_point_diff)
        drink_stam()
        plant_seed(14)
        get_in_position_v2(anchor, modified_start_point_diff)
        water_plant(14, '27387')
        get_in_position_v2(anchor, modified_start_point_diff)
        drink_stam()
        water_plant(14, '27390')
        get_in_position_v2(anchor, modified_start_point_diff)
        drink_stam()
        water_plant(14, '27393')
        get_in_position_v2(anchor, deposit_sack)
        iters_14 += 1
    iters_15 = 0
    while iters_15 < 2:
        fill_watering_cans()
        get_in_position_v2(anchor, start_point_diff)
        drink_stam()
        plant_seed(15)
        get_in_position_v2(anchor, modified_start_point_diff)
        drink_stam()
        water_plant(15, '27387')
        get_in_position_v2(anchor, modified_start_point_diff)
        water_plant(15, '27390')
        get_in_position_v2(anchor, modified_start_point_diff)
        drink_stam()
        water_plant(15, '27393')
        get_in_position_v2(anchor, deposit_sack)
        iters_15 += 1
    deposit_fruit()
    leave_game()

main()