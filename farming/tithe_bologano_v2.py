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
    'y': -14
}

modified_start_point_diff = {
    'x': 5,
    'y': -12
}

deposit_sack = {
    'x': 1,
    'y': 1
}


def fill_watering_cans():
    inv = osrs.inv.get_inv(port)
    grico = osrs.inv.is_item_in_inventory_v2(inv, 13353)
    if grico:
        osrs.move.move_and_click(grico['x'], grico['y'], 3, 3)
        water = osrs.server.get_surrounding_game_objects(10, ['5598'], port)
        if '5598' in water:
            osrs.move.move_and_click(water['5598']['x'], water['5598']['y'], 2, 2)
            osrs.clock.random_sleep(2, 3)
            return

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
    osrs.move.run_towards_square_v2({'x': anchor['x_coord'] + diff['x'], 'y': anchor['y_coord'] + diff['y'], 'z': 0}, port)


def run_to_fifth_row():
    loc = osrs.server.get_world_location(port)
    osrs.move.run_towards_square_v2({'x': loc['x'] + 6, 'y': loc['y'] - 12, 'z': 0}, port)


def place_seed_in_patch():
    inv = osrs.inv.get_inv(port)
    seed = osrs.inv.is_item_in_inventory_v2(inv, BOLOGANO_SEED)
    osrs.move.move_and_click(seed['x'], seed['y'], 3, 3)
    patches = osrs.server.get_multiple_surrounding_game_objects(10, [EMPTY_PATCH], port)
    # {'x': 885, 'y': 579, 'dist': 2, 'x_coord': 15330, 'y_coord': 2584}
    closest = osrs.util.find_closest_target(patches[EMPTY_PATCH])
    osrs.move.move_and_click(closest['x'], closest['y'], 2, 2)
    start_time = datetime.datetime.now()
    while True:
        planted_patch = osrs.server.get_game_object(
            '{},{},0'.format(closest['x_coord'], closest['y_coord']),
            UNWATERED_SEED_STAGE_1,
            port
        )
        if planted_patch:
            return planted_patch
        elif (datetime.datetime.now() - start_time).total_seconds() > 4:
            return False


# spam clicking water here cancels the action and you never actually water it
def water_new_seed(seed):
    osrs.move.move_and_click(seed['x'], seed['y'], 3, 3)
    start_time = datetime.datetime.now()
    while True:
        watered = osrs.server.get_game_object('{},{},0'.format(seed['x_coord'], seed['y_coord']), WATERED_STAGE_1, port)
        if watered:
            return True
        elif (datetime.datetime.now() - start_time).total_seconds() > 4:
            return False


def plant_seed(amount):
    planted = 0
    while planted < amount:
        while True:
            fresh_seed = place_seed_in_patch()
            if fresh_seed:
                while True:
                    watered = water_new_seed(fresh_seed)
                    if watered:
                        planted += 1
                        break
                break


def water_plant(amount, nominal_state):
    start_time = datetime.datetime.now()
    planted = 0
    blighted = 0
    #  or (start_time - datetime.datetime.now()).total_seconds() < 75
    while planted + blighted < amount:
        patches = osrs.server.get_multiple_surrounding_game_objects(
            10,
            [nominal_state, BLIGHTED_STAGE_1, BLIGHTED_STAGE_2, BLIGHTED_STAGE_3, BLIGHTED_STAGE_4],
            port
        )
        possible_objs = []
        if bool(patches):
            for key in patches:
                possible_objs += patches[key]
                closest = osrs.util.find_closest_target(possible_objs)
                osrs.move.move_and_click(closest['x'], closest['y'], 3, 3)
                start_time = datetime.datetime.now()
                while True:
                    clicked = osrs.server.get_game_object(
                        '{},{},0'.format(closest['x_coord'], closest['y_coord']),
                        str(closest['id']),
                        port
                    )
                    if not clicked:
                        if str(closest['id']) in [BLIGHTED_STAGE_1, BLIGHTED_STAGE_2, BLIGHTED_STAGE_3, BLIGHTED_STAGE_4]:
                            blighted += 1
                        else:
                            planted += 1
                        break
                    elif (datetime.datetime.now() - start_time).total_seconds() > 4:
                        break
    return blighted


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


script_config = {

    'intensity': 'low',
    'logout': False,
    'login': False,
    'click_to_play': False

}


def main():
    while True:
        total_blighted = 0
        osrs.game.break_manager_v3(script_config)
        anchor = determine_anchor_tile()
        fill_watering_cans()
        get_in_position_v2(anchor, start_point_diff)
        drink_stam()
        plant_seed(16 - total_blighted)
        get_in_position_v2(anchor, modified_start_point_diff)
        blighted = water_plant(16, UNWATERED_SEED_STAGE_2)
        total_blighted += blighted
        get_in_position_v2(anchor, modified_start_point_diff)
        drink_stam()
        blighted = water_plant(16 - total_blighted, UNWATERED_SEED_STAGE_3)
        total_blighted += blighted
        get_in_position_v2(anchor, modified_start_point_diff)
        drink_stam()
        water_plant(16 - total_blighted, HEALTHY_STAGE_4)
        get_in_position_v2(anchor, deposit_sack)


main()
