import datetime

from osrs_utils import general_utils
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
    ground_items = general_utils.get_surrounding_ground_items(5, ['954'], port)
    if ground_items and '954' in ground_items:
        general_utils.right_click_menu_select(ground_items['954'][0], None, port, 'Rope', 'Take')
        general_utils.sleep_one_tick()
        general_utils.wait_until_stationary(port)
        general_utils.sleep_one_tick()
        found_rope = True
    ground_items = general_utils.get_surrounding_ground_items(2, ['303'], port)
    if ground_items and '303' in ground_items:
        general_utils.right_click_menu_select(ground_items['303'][0], None, port, 'Small fishing net', 'Take')
        general_utils.sleep_one_tick()
        general_utils.wait_until_stationary(port)
        general_utils.sleep_one_tick()
        found_net = True
    return found_rope and found_net


def find_catches():
    objs = general_utils.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8734'], port)
    if '8734' in objs:
        closest = general_utils.find_closest_target(objs['8734'])
        general_utils.move_and_click(closest['x'], closest['y'], 2, 2)
        general_utils.sleep_one_tick()
        general_utils.wait_until_stationary(port)
        general_utils.sleep_one_tick()
        return True
    return False


def find_traps():
    objs = general_utils.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8731'], port)
    if '8731' in objs:
        if len(objs['8731']) < min_traps:
            # these are temp trap states i want to wait until they are settled
            bad_objs = general_utils.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8733', '8974', '8973', '8972'], port)
            if not bool(bad_objs):
                place_trap()
    else:
        place_trap()


def place_trap():
    tree = general_utils.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8732'], port)
    if tree and '8732' in tree:
        closest = general_utils.find_closest_target(tree['8732'])
        general_utils.move_and_click(closest['x'], closest['y'], 2, 2)
        general_utils.sleep_one_tick()
        general_utils.wait_until_stationary(port)
        general_utils.sleep_one_tick()


def end_traps():
    objs = general_utils.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8731'], port)
    bad_objs = general_utils.get_game_objects_in_coords(x_min, x_max, y_min, y_max, z, ['8733', '8974', '8973', '8972'], port)
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
        if cycles_with_no_findings >= min_traps and end_traps():
            break


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 51, 56, 423, 551, 'pass_70', False, port, retrieve_traps_for_logout)
        general_utils.wait_until_stationary(port)
        find_broken_traps()
        find_catches()
        find_traps()
        general_utils.deposit_all_of_x([10146], port)


main()