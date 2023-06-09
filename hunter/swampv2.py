import datetime


import osrs
min_traps = 2
port = '56799'

def find_broken_traps():
    found_rope = False
    found_net = False
    ground_items = osrs.server.get_surrounding_ground_items(5, ['954'], port)
    if ground_items and '954' in ground_items:
        osrs.move.right_click_menu_select(ground_items['954'][0], None, port, 'Rope', 'Take')
        osrs.clock.sleep_one_tick()
        osrs.move.wait_until_stationary(port)
        osrs.clock.sleep_one_tick()
        found_rope = True
    ground_items = osrs.server.get_surrounding_ground_items(5, ['303'], port)
    if ground_items and '303' in ground_items:
        osrs.move.right_click_menu_select(ground_items['303'][0], None, port, 'Small fishing net', 'Take')
        osrs.clock.sleep_one_tick()
        osrs.move.wait_until_stationary(port)
        osrs.clock.sleep_one_tick()
        found_net = True
    return found_rope and found_net

def find_catches():
    objs = osrs.server.get_surrounding_game_objects(5, ['9004'])
    if '9004' in objs:
        osrs.move.move_and_click(objs['9004']['x'], objs['9004']['y'], 2, 2)
        osrs.clock.random_sleep(2.3, 2.4)
        return True
    return False

def find_traps():
    objs = osrs.server.get_multiple_surrounding_game_objects(5, ['9343'])
    if '9343' in objs:
        if len(objs['9343']) < min_traps:
            # these are temp trap states i want to wait until they are settled
            bad_objs = osrs.server.get_surrounding_game_objects(8, ['9003', '9004', '9005', '9158'])
            if not bool(bad_objs):
                place_trap()
    else:
        place_trap()


def place_trap():
    tree = osrs.server.get_surrounding_game_objects(5, ['9341'])
    if tree and '9341' in tree:
        osrs.move.move_and_click(tree['9341']['x'], tree['9341']['y'], 2, 2)
        osrs.clock.random_sleep(4, 5)


def end_traps():
    objs = osrs.server.get_multiple_surrounding_game_objects(5, ['9343'])
    bad_objs = osrs.server.get_surrounding_game_objects(8, ['9003', '9004', '9005', '9158'])
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
        start_time = osrs.game.break_manager(start_time, 51, 56, 423, 551, 'pass_70', False, port, retrieve_traps_for_logout)
        osrs.move.wait_until_stationary(port)
        find_broken_traps()
        find_catches()
        find_traps()
        osrs.bank.deposit_all_of_x([10149], port)


main()