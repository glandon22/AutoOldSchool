import datetime


import osrs, keyboard

port = '56799'
BOLOGANO_SEED = '13424'
EMPTY_PATCH = '27383'

UNWATERED_SEED_STAGE_1 = '27395'
WATERED_STAGE_1 = '27396'
BLIGHTED_STAGE_1 = '27397'

UNWATERED_SEED_STAGE_2 = '27398'
WATERED_STAGE_2 = '27399'
BLIGHTED_STAGE_2 = '27400'

UNWATERED_SEED_STAGE_3 = '27401'
WATERED_STAGE_3 = '27402'
BLIGHTED_STAGE_3 = '27403'

HEALTHY_STAGE_4 = '27404'
BLIGHTED_STAGE_4 = '27405'

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


def fill_watering_cans():
    while True:
        inv = osrs.inv.get_inv(port)
        not_full_can = osrs.inv.are_items_in_inventory_v2(inv, [5331, 5333, 5334, 5335, 5336, 5337, 5338, 5339])
        if not_full_can:
            osrs.move.move_and_click(not_full_can['x'], not_full_can['y'], 3, 3)
            water = osrs.server.get_surrounding_game_objects(10, ['5598'], port)
            if '5598' in water:
                osrs.move.move_and_click(water['5598']['x'], water['5598']['y'], 2, 2)
                osrs.clock.random_sleep(0.6, 0.7)
        else:
            break


def deposit_fruit():
    while True:
        inv = osrs.inv.get_inv(port)
        sack = osrs.server.get_surrounding_game_objects(5, ['27431'], port)
        if '27431' in sack:
            osrs.move.move_and_click(sack['27431']['x'], sack['27431']['y'], 2, 2)
            osrs.clock.random_sleep(0.6, 0.7)
            while True:
                if inv != osrs.inv.get_inv(port, True):
                    return


def get_in_position_v2(anchor, diff):
    osrs.move.run_towards_square({'x': anchor['x_coord'] + diff['x'], 'y': anchor['y_coord'] + diff['y'], 'z': 0}, port)


def run_to_fifth_row():
    loc = osrs.server.get_world_location(port)
    osrs.move.run_towards_square({'x': loc['x'] + 6, 'y': loc['y'] - 12, 'z': 0}, port)


def plant_seed(amount):
    planted = 0
    while planted < amount:
        inv = osrs.inv.get_inv(port)
        seed = osrs.inv.is_item_in_inventory_v2(inv, BOLOGANO_SEED)
        starting_seed_quant = seed['quantity']
        osrs.move.move_and_click(seed['x'], seed['y'], 3, 3)
        patches = osrs.server.get_multiple_surrounding_game_objects(10, [EMPTY_PATCH], port)
        closest = osrs.util.find_closest_target(patches[EMPTY_PATCH])
        osrs.move.move_and_click(closest['x'], closest['y'], 2, 2)
        while True:
            inv = osrs.inv.get_inv(port, True)
            seed = osrs.inv.is_item_in_inventory_v2(inv, BOLOGANO_SEED)
            if not seed or seed['quantity'] != starting_seed_quant:
                break
        '''watering_can = osrs.inv.are_items_in_inventory_v2(inv, [5340, 5333, 5334, 5335, 5336, 5337, 5338, 5339])
        osrs.move.move_and_click(watering_can['x'], watering_can['y'], 3, 3)'''
        patches = osrs.server.get_multiple_surrounding_game_objects(2, [UNWATERED_SEED_STAGE_1], port)
        closest = osrs.util.find_closest_target(patches[UNWATERED_SEED_STAGE_1])
        osrs.move.move_and_click(closest['x'], closest['y'], 2, 2)
        osrs.clock.random_sleep(0.6, 0.7)
        planted += 1


def water_plant(amount, obj_id):
    planted = 0
    while planted < amount:
        inv = osrs.inv.get_inv(port)
        blighted = False
        while True:
            patches = osrs.server.get_multiple_surrounding_game_objects(10, [obj_id, BLIGHTED_STAGE_1, BLIGHTED_STAGE_2, BLIGHTED_STAGE_3, BLIGHTED_STAGE_4], port)
            possible_objs = []
            if bool(patches):
                if obj_id in patches:
                    possible_objs = patches[obj_id] + possible_objs
                if BLIGHTED_STAGE_1 in patches:
                    blighted = True
                    possible_objs = patches[BLIGHTED_STAGE_1] + possible_objs
                if BLIGHTED_STAGE_2 in patches:
                    blighted = True
                    possible_objs = patches[BLIGHTED_STAGE_2] + possible_objs
                if BLIGHTED_STAGE_3 in patches:
                    blighted = True
                    possible_objs = patches[BLIGHTED_STAGE_3] + possible_objs
                if BLIGHTED_STAGE_4 in patches:
                    blighted = True
                    possible_objs = patches[BLIGHTED_STAGE_4] + possible_objs
                closest = osrs.util.find_closest_target(possible_objs)
                osrs.move.move_and_click(closest['x'], closest['y'], 2, 2)
                break
        start = datetime.datetime.now()
        while True:
            curr_inv = osrs.inv.get_inv(port)
            if inv != curr_inv or blighted or (datetime.datetime.now() - start).total_seconds() > 9:
                break
        osrs.clock.random_sleep(0.7, 0.8)
        planted += 1

def determine_anchor_tile():
    while True:
        water = osrs.server.get_surrounding_game_objects(10, ['5598'], port)
        if '5598' in water:
            return water['5598']


def drink_stam():
    run_energy = osrs.server.get_widget('160,28', port)
    if run_energy and int(run_energy['text']) < 35:
        inv = osrs.inv.get_inv(port, True)
        stam = osrs.inv.are_items_in_inventory_v2(inv, [12631, 12629, 12627, 12625])
        if stam:
            osrs.move.move_and_click(stam['x'], stam['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.1)


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 53, 57, 423, 551, 'pass_70', False, click_to_play=False)
        anchor = determine_anchor_tile()
        fill_watering_cans()
        get_in_position_v2(anchor, start_point_diff)
        drink_stam()
        plant_seed(16)
        get_in_position_v2(anchor, modified_start_point_diff)
        water_plant(16, UNWATERED_SEED_STAGE_2)
        get_in_position_v2(anchor, modified_start_point_diff)
        drink_stam()
        water_plant(16, UNWATERED_SEED_STAGE_3)
        get_in_position_v2(anchor, modified_start_point_diff)
        drink_stam()
        water_plant(16, HEALTHY_STAGE_4)
        get_in_position_v2(anchor, deposit_sack)


main()

# cant currently do this due to how i check if a seed is planted / watered. inv does not change
''' # If I have Gricoller's can - use that only
 inv = osrs.inv.get_inv(port)
 grico = osrs.inv.is_item_in_inventory_v2(inv, 13353)
 if grico:
     osrs.move.move_and_click(grico['x'], grico['y'], 3, 3)
     water = osrs.server.get_surrounding_game_objects(10, ['5598'], port)
     if '5598' in water:
         osrs.move.move_and_click(water['5598']['x'], water['5598']['y'], 2, 2)
         osrs.clock.random_sleep(2, 3)
         return'''