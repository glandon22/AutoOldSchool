import datetime


import osrs
min_traps = 3
port = '56799'
x_min = 3402
x_max = 3409
y_min = 3087
y_max = 3094
z = 0


def find_broken_traps():
    found_rope = False
    found_net = False
    ground_items = osrs.server.get_surrounding_ground_items(8, ['954'], port)
    if ground_items and '954' in ground_items:
        closest = osrs.util.find_closest_target(ground_items['954'])
        osrs.move.right_click_menu_select(closest, None, port, 'Rope', 'Take')
        osrs.clock.sleep_one_tick()
        osrs.move.wait_until_stationary(port)
        osrs.clock.sleep_one_tick()
        found_rope = True
    ground_items = osrs.server.get_surrounding_ground_items(8, ['303'], port)
    if ground_items and '303' in ground_items:
        closest = osrs.util.find_closest_target(ground_items['303'])
        osrs.move.right_click_menu_select(closest, None, port, 'Small fishing net', 'Take')
        osrs.clock.sleep_one_tick()
        osrs.move.wait_until_stationary(port)
        osrs.clock.sleep_one_tick()
        found_net = True
    return found_rope and found_net

def find_all_broken_traps():
    found = False
    while True:
        ground_items = osrs.server.get_surrounding_ground_items(8, ['954', '303'], port)
        items = []
        if ground_items and '954' in ground_items:
            items += ground_items['954']
            found = True
        if ground_items and '303' in ground_items:
            items += ground_items['303']
            found = True

        if len(items) > 0:
            closest = osrs.util.find_closest_target(items)
            osrs.move.right_click_menu_select(closest, None, port, 'e', 'Take')
            start_time = datetime.datetime.now()
            prev_inv = osrs.inv.get_inv(port)
            while True:
                inv = osrs.inv.get_inv(port)
                if inv != prev_inv:
                    break
                elif (datetime.datetime.now() - start_time).total_seconds() > 5:
                    break
        else:
            break
    return found


def find_catches():
    objs = osrs.server.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8734'], port)
    if '8734' in objs:
        closest = osrs.util.find_closest_target(objs['8734'])
        prev_inv = osrs.inv.get_inv(port)
        osrs.move.move_and_click(closest['x'], closest['y'], 2, 2)
        start_time = datetime.datetime.now()
        while True:
            inv = osrs.inv.get_inv(port)
            if inv != prev_inv:
                osrs.clock.sleep_one_tick()
                break
            elif (datetime.datetime.now() - start_time).total_seconds() > 7:
                break
        osrs.bank.deposit_all_of_x([10146], port)
        return True
    return False


def find_traps():
    objs = osrs.server.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8731'], port)
    if '8731' in objs:
        if len(objs['8731']) < min_traps:
            # these are temp trap states i want to wait until they are settled
            bad_objs = osrs.server.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8733', '8974', '8973', '8972'], port)
            if not bool(bad_objs):
                place_trap()
    else:
        place_trap()


def place_trap():
    tree = osrs.server.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8732'], port)
    if tree and '8732' in tree:
        prev_inv = osrs.inv.get_inv(port)
        if not osrs.inv.is_item_in_inventory_v2(prev_inv, 954):
            return
        if not osrs.inv.is_item_in_inventory_v2(prev_inv, 303):
            return
        closest = osrs.util.find_closest_target(tree['8732'])
        osrs.move.move_and_click(closest['x'], closest['y'], 2, 2)
        start_time = datetime.datetime.now()
        while True:
            inv = osrs.inv.get_inv(port)
            if inv != prev_inv:
                osrs.clock.sleep_one_tick()
                break
            elif (datetime.datetime.now() - start_time).total_seconds() > 7:
                break


def end_traps():
    objs = osrs.server.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8731'], port)
    bad_objs = osrs.server.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8733', '8974', '8973', '8972'], port)
    if '9343' not in objs and not bool(bad_objs):
        return True
    else:
        return False


def retrieve_traps_for_logout():
    cycles_with_no_findings = 0
    while True:
        broken = find_broken_traps()
        catches = find_catches()
        if not broken and not catches and end_traps():
            cycles_with_no_findings += 1
        else:
            cycles_with_no_findings = 0
        if cycles_with_no_findings >= 15 and end_traps():
            break


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 51, 56, 423, 551, 'julenth', False, port, retrieve_traps_for_logout)
        osrs.move.wait_until_stationary(port)
        find_traps()
        bkn = find_broken_traps()
        if bkn:
            place_trap()
        fc = find_catches()
        if fc:
            place_trap()

main()