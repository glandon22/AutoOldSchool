import datetime

from osrs_utils import general_utils
# broken snare to be picked up 9344
# placed snare waiting for bird 9345
# 9348 cautgh cerulean
# 9346 temp state right before trap breaks when bird lands
# temp state right before brid is caught 9347
# you get bones, raw bird meat
# cetner tile 1553, 3438,0 placing a trap always moves you to the left
# bird snare in inv 10006
port = '56799'
def place_trap():
    loc = general_utils.get_world_location(port)
    if loc and 'x' in loc and loc['x'] < 2535:
        general_utils.run_to_loc(['2539,2885,0'], port)
    inv = general_utils.get_inv(port, True)
    snare = general_utils.is_item_in_inventory_v2(inv, 10006)
    if snare:
        general_utils.move_and_click(snare['x'], snare['y'], 3, 3)
        general_utils.random_sleep(2, 2.3)
    while True:
        objs = general_utils.get_surrounding_game_objects(3, ['9345'])
        if '9345' in objs:
            break
    meat = general_utils.is_item_in_inventory_v2(inv, 9978)
    if meat:
        general_utils.move_and_click(meat['x'], meat['y'], 3, 3)
    bones = general_utils.is_item_in_inventory_v2(inv, 526)
    if bones:
        general_utils.move_and_click(bones['x'], bones['y'], 3, 3)

def wait_for_catch():
    while True:
        objs = general_utils.get_surrounding_game_objects(3, ['9344', '9345', '9348', '9346', '9347'])
        if '9344' in objs:
            general_utils.move_and_click(objs['9344']['x'], objs['9344']['y'], 2, 2)
            general_utils.random_sleep(2, 2.3)
            break
        elif '9348' in objs:
            general_utils.move_and_click(objs['9348']['x'], objs['9348']['y'], 2, 2)
            general_utils.random_sleep(2, 2.3)
            break
        # check if none of these objects are present
        elif not bool(objs):
            snare = general_utils.get_surrounding_ground_items(3, ['10006'], port)
            print(snare)
            if '10006' in snare:
                general_utils.right_click_menu_select(snare['10006'][0], None, port, 'Bird snare', 'Take')
            break

def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 58, 423, 551, 'julenth', False)
        general_utils.random_sleep(0.6, 0.7)
        place_trap()
        general_utils.random_sleep(0.6, 0.7)
        wait_for_catch()

general_utils.random_sleep(1, 1.5)
main()
