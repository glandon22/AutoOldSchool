import datetime


import osrs

port = '56799'
course_start = {
    'x': 2626,
    'y': 3677,
    'z': 0
}


def click_allowed(lc, cd, step):
    print('lc', lc)
    # this is not the last clicked step
    if lc['step'] != step:
        return True
    now = datetime.datetime.now()
    if (now - lc['ts']).total_seconds() > cd:
        return True
    else:
        return False


def start_course(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 0 and click_allowed(lc, 3, 1):
        osrs.clock.sleep_one_tick()
        q = {
            'decorativeObjects': [{
                'tile': '2625,3677,0',
                'object': '14946'
            }]
        }
        data = osrs.server.query_game_data(q)
        if 'decorativeObjects' in data and '14946' in data['decorativeObjects']:
            osrs.move.move_and_click(data['decorativeObjects']['14946'][0]['x'],
                                         data['decorativeObjects']['14946'][0]['y'], 2, 2)
            osrs.clock.sleep_one_tick()
            osrs.move.wait_until_stationary(port)
            osrs.clock.sleep_one_tick()
            return {
                'step': 1,
                'ts': datetime.datetime.now()
            }
        else:
            osrs.move.run_towards_square(course_start, port)
    return lc


def platform_1(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            2622 <= loc['x'] <= 2626 and \
            3672 <= loc['y'] <= 3676 and \
            click_allowed(lc, 4, 2):
        osrs.agil.handle_marks(2622, 2626, 3672, 3676, 3, port)
        obstacle = osrs.server.get_game_object('2623,3671,3', '14947', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 2,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_2(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            2615 <= loc['x'] <= 2622 and \
            3658 <= loc['y'] <= 3668 and \
            click_allowed(lc, 4, 3):
        osrs.agil.handle_marks(2615, 2622, 3658, 3668, 3, port)
        obstacle = osrs.server.get_game_object('2623,3658,3', '14987', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 3,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_3(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            2626 <= loc['x'] <= 2630 and \
            3651 <= loc['y'] <= 3655 and \
            click_allowed(lc, 4, 4):
        osrs.agil.handle_marks(2626, 2630, 3651, 3655, 3, port)
        obstacle = osrs.server.get_game_object('2629,3656,3', '14990', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(0.6, 0.7)
            return {
                'step': 4,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_4(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            2639 <= loc['x'] <= 2644 and \
            3649 <= loc['y'] <= 3653 and \
            click_allowed(lc, 4, 4):
        osrs.agil.handle_marks(2639, 2644, 3649, 3653, 3, port)
        obstacle = osrs.server.get_game_object('2643,3654,3', '14991', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 5,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_5(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            2643 <= loc['x'] <= 2650 and \
            3656 <= loc['y'] <= 3662 and \
            click_allowed(lc, 3, 6):
        # animatino delay
        osrs.clock.sleep_one_tick()
        osrs.agil.handle_marks(2643, 2650, 3656, 3662, 3, port)
        obstacle = osrs.server.get_game_object('2647,3663,3', '14992', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 6,
                'ts': datetime.datetime.now()
            }
    return lc


def platform_6(lc):
    loc = osrs.server.get_world_location(port)
    if 'z' in loc and loc['z'] == 3 and \
            2655 <= loc['x'] <= 2666 and \
            3665 <= loc['y'] <= 3685 and \
            click_allowed(lc, 5, 7):
        osrs.agil.handle_marks(2655, 2666, 3665, 3685, 3, port)
        obstacle = osrs.server.get_game_object('2654,3676,3', '14994', port)
        if bool(obstacle):
            osrs.move.move_and_click(obstacle['x'], obstacle['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.2)
            return {
                'step': 7,
                'ts': datetime.datetime.now()
            }
    return lc


def drink_stam():
    run_energy = osrs.server.get_widget('160,28', port)
    if run_energy and int(run_energy['text']) < 45:
        inv = osrs.inv.get_inv(port, True)
        stam = osrs.inv.are_items_in_inventory_v2(inv, [12631, 12629, 12627, 12625])
        if stam:
            osrs.move.move_and_click(stam['x'], stam['y'], 3, 3)
            osrs.clock.random_sleep(1, 1.1)


def drink_wine():
    hp = osrs.server.get_skill_data('hitpoints', port)
    if 'boostedLevel' in hp and hp['boostedLevel'] < 2:
        inv = osrs.inv.get_inv(port)
        wine = osrs.inv.is_item_in_inventory_v2(inv, '26149')
        if not wine:
            exit('out of wine')
        osrs.move.move_and_click(wine['x'], wine['y'], 3, 3)


def main():
    last_click = {
        'step': 0,
        'ts': datetime.datetime.now()
    }
    start_time = datetime.datetime.now()
    while True:
        start_time = osrs.game.break_manager(start_time, 43, 48, 423, 551, 'julenth', False)
        osrs.move.wait_until_stationary(port)
        drink_stam()
        drink_wine()
        last_click = start_course(last_click)
        last_click = platform_1(last_click)
        last_click = platform_2(last_click)
        last_click = platform_3(last_click)
        last_click = platform_4(last_click)
        last_click = platform_5(last_click)
        last_click = platform_6(last_click)

main()