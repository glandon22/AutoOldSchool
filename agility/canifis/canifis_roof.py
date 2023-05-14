import datetime

import keyboard

from autoscape import general_utils
import canifis_vars as mog_tiles

# i think leveling up freezes me, may need to handle that
# called if i fall to get in range of course start
def go_to_center():
    q = {
        'tiles': ['3493,3488,0']
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'tiles' in data and '349334880' in data['tiles']:
            general_utils.move_and_click(data['tiles']['349334880']['x'], data['tiles']['349334880']['y'], 7, 7)
            general_utils.random_sleep(1.5, 1.6)
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break

def ground_item_payload_generator(tiles):
    q = {
        'groundItems': []
    }
    for tile in tiles:
        q['groundItems'].append({
            'tile': tile,
            'object': '11849'
        })
    return q


def handle_marks(area):
    q = ground_item_payload_generator(area)
    data = general_utils.query_game_data(q)
    if 'groundItems' in data and bool(data['groundItems']) and '11849' in data['groundItems']:
        # screen is moving since im running, wait a second for the screen to settle so i dont miss mark
        general_utils.random_sleep(1, 1.1)
        q = ground_item_payload_generator(area)
        data = general_utils.query_game_data(q)
        mark = data['groundItems']['11849'][0]
        general_utils.move_and_click(mark['x'], mark['y'], 2, 3)
        general_utils.random_sleep(0.5, 0.6)
        general_utils.wait_until_stationary()
        general_utils.random_sleep(1.5, 1.6)
        return True
    return False

# left off here
def click_course_start():
    q = {
        'tiles': ['3508,3489,0']
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'tiles' in data and '350834890' in data['tiles']:
            general_utils.move_and_click(data['tiles']['350834890']['x'],
                                         data['tiles']['350834890']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step1():
    click_course_start()
    # in this loop, i need to check if i have leveled. if i have hold space for a couple seconds to get dialogue off
    while True:
        q = {
            'playerWorldPoint': True,
            'poseAnimation': True
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data \
                and data['playerWorldPoint']['x'] == 3506 \
                and data['playerWorldPoint']['y'] == 3492 \
                and data['playerWorldPoint']['z'] > 0:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_1_tiles)
            break


def click_step2():
    q = {
        'gameObjects': [{
            'tile': '3506,3498,2',
            'object': '14844'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14844' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14844']['x'], data['gameObjects']['14844']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break

def step2():
    click_step2()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['y'] == 3504:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_2_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell on step 2.')
            return 'fell'
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step2()
    # afterwards do a scan for any marks of grace


def click_step3():
    q = {
        'gameObjects': [{
            'tile': '3496,3504,2',
            'object': '14845'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14845' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14845']['x'], data['gameObjects']['14845']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step3():
    click_step3()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3492 and data['playerWorldPoint']['y'] == 3504:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_3_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step3()
    # afterwards do a scan for any marks of grace


def click_step4():
    q = {
        'gameObjects': [{
            'tile': '3485,3499,2',
            'object': '14848'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14848' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14848']['x'], data['gameObjects']['14848']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step4():
    click_step4()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3479 and data['playerWorldPoint']['y'] == 3499:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(1.5, 1.6)
            handle_marks(mog_tiles.area_4_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell on step 4.')
            return 'fell'
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step4()


def click_step5():
    q = {
        'gameObjects': [{
            'tile': '3478,3491,3',
            'object': '14846'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14846' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14846']['x'], data['gameObjects']['14846']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step5():
    click_step5()
    while True:
        q = {
            'playerWorldPoint': True
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3478 and data['playerWorldPoint']['y'] == 3486:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_5_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step5()


def click_step6():
    q = {
        'gameObjects': [{
            'tile': '3480,3483,2',
            'object': '14894'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14894' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14894']['x'], data['gameObjects']['14894']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step6():
    click_step6()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3489 and data['playerWorldPoint']['y'] == 3476:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_6_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step6()


def click_step7():
    q = {
        'gameObjects': [{
            'tile': '3504,3476,3',
            'object': '14847'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14847' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14847']['x'], data['gameObjects']['14847']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step7():
    click_step7()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3510:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_7_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell on step 7.')
            return 'fell'
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step7()


def click_step8():
    q = {
        'gameObjects': [{
            'tile': '3510,3483,2',
            'object': '14897'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14897' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14897']['x'], data['gameObjects']['14897']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step8():
    click_step8()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3510 and data['playerWorldPoint']['y'] == 3485:
            general_utils.wait_until_stationary()
            break
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step8()


def look_up():
    keyboard.press('up')
    general_utils.random_sleep(1, 1.2)
    keyboard.release('up')


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 47, 54, 423, 551, 'pass_70', look_up)
        fell7 = False
        fell4 = False
        step1()
        step2()
        step3()
        fell4 = step4()
        if fell4 == 'fell':
            general_utils.random_sleep(3.3, 3.4)
            go_to_center()
            continue
        general_utils.random_sleep(0.5, 0.6)
        step5()
        step6()
        fell7 = step7()
        if fell7 == 'fell':
            general_utils.random_sleep(3, 3.4)
            continue
        step8()
        general_utils.random_sleep(1, 1.2)


main()