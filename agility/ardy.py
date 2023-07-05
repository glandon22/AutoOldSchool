import datetime


import osrs
import osrs
port = '56799'
course_start = {
    'x': 2673,
    'y': 3298,
    'z': 0
}


# wait a few seconds before logging out in case i am in an obstacle
def logout():
    osrs.clock.random_sleep(10, 11)


script_config = {
    'intensity': 'high',
    'logout': logout,
    'login': False
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
                'tile': '2673,3298,0',
                'object': '15608'
            }]
        }
        data = osrs.server.query_game_data(q)
        if 'decorativeObjects' in data and '15608' in data['decorativeObjects']:
            osrs.move.move_and_click(data['decorativeObjects']['15608'][0]['x'],
                                         data['decorativeObjects']['15608'][0]['y'], 2, 2)
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
            2671 <= loc['x'] <= 2672 and \
            3299 <= loc['y'] <= 3309 and \
            click_allowed(lc, 5, 2):
        obstacle = osrs.server.get_game_object('2671,3310,3', '15609', port)
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
            2661 <= loc['x'] <= 2665 and \
            3318 <= loc['y'] <= 3319 and \
            click_allowed(lc, 4, 3):
        # Additional animation delay
        osrs.clock.random_sleep(0.6, 0.7)
        obstacle = osrs.server.get_ground_object('2661,3318,3', '26635', port)
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
            2653 <= loc['x'] <= 2657 and \
            3318 <= loc['y'] <= 3319 and \
            click_allowed(lc, 4, 4):
        osrs.agil.handle_marks(2653, 2657, 3318, 3319, 3, port)
        obstacle = osrs.server.get_game_object('2653,3318,3', '15610', port)
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
            2653 <= loc['x'] <= 2654 and \
            3310 <= loc['y'] <= 3314 and \
            click_allowed(lc, 4, 5):
        obstacle = osrs.server.get_game_object('2653,3309,3', '15611', port)
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
            2651 <= loc['x'] <= 2653 and \
            3300 <= loc['y'] <= 3309 and \
            click_allowed(lc, 3, 6):
        # animatino delay
        osrs.clock.sleep_one_tick()
        obstacle = osrs.server.get_game_object('2654,3300,3', '28912', port)
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
            3297 <= loc['y'] <= 3297 and \
            click_allowed(lc, 5, 7):
        obstacle = osrs.server.get_game_object('2656,3296,3', '15612', port)
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
    if 'boostedLevel' in hp and hp['boostedLevel'] < 15:
        inv = osrs.inv.get_inv(port)
        wine = osrs.inv.is_item_in_inventory_v2(inv, '1993')
        if not wine:
            exit('out of wine')
        osrs.move.move_and_click(wine['x'], wine['y'], 3, 3)


def main():
    last_click = {
        'step': 0,
        'ts': datetime.datetime.now()
    }
    while True:
        osrs.game.break_manager_v3(script_config)
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