
import osrs
# broken snare to be picked up 9344
# placed snare waiting for bird 9345
# caught bird 9379
# 9346 temp state right before trap breaks when bird lands
# 9378 temp state right before brid is caught
# you get bones, raw bird meat
# cetner tile 1553, 3438,0 placing a trap always moves you to the left
# bird snare in inv 10006
port = '56799'
def place_trap():
    loc = osrs.server.get_world_location(port)
    if loc and 'x' in loc and loc['x'] < 1551:
        osrs.move.run_to_loc(['1553,3438,0'], port)
    inv = osrs.inv.get_inv(port, True)
    snare = osrs.inv.is_item_in_inventory_v2(inv, 10006)
    if snare:
        osrs.move.move_and_click(snare['x'], snare['y'], 3, 3)
        osrs.clock.random_sleep(2, 2.3)
    while True:
        objs = osrs.server.get_surrounding_game_objects(3, ['9345'])
        if '9345' in objs:
            break
    meat = osrs.inv.is_item_in_inventory_v2(inv, 9978)
    if meat:
        osrs.move.move_and_click(meat['x'], meat['y'], 3, 3)
    bones = osrs.inv.is_item_in_inventory_v2(inv, 526)
    if bones:
        osrs.move.move_and_click(bones['x'], bones['y'], 3, 3)

def wait_for_catch():
    while True:
        objs = osrs.server.get_surrounding_game_objects(3, ['9344', '9345', '9379', '9346', '9378'])
        if '9344' in objs:
            osrs.move.move_and_click(objs['9344']['x'], objs['9344']['y'], 2, 2)
            osrs.clock.random_sleep(2, 2.3)
            break
        elif '9379' in objs:
            osrs.move.move_and_click(objs['9379']['x'], objs['9379']['y'], 2, 2)
            osrs.clock.random_sleep(2, 2.3)
            break
        # check if none of these objects are present
        elif not bool(objs):
            snare = osrs.server.get_surrounding_ground_items(3, ['10006'], port)
            print(snare)
            if '10006' in snare:
                osrs.move.right_click_menu_select(snare['10006'][0], None, port, 'Bird snare', 'Take')
            break

def main():
    while True:
        osrs.clock.random_sleep(0.6, 0.7)
        place_trap()
        osrs.clock.random_sleep(0.6, 0.7)
        wait_for_catch()

osrs.clock.random_sleep(1, 1.5)
main()
