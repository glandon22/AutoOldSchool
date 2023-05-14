import datetime

import keyboard

from autoscape import general_utils
import varrock_vars as mog_tiles

# i think leveling up freezes me, may need to handle that
# called if i fall to get in range of course start
def go_to_center():
    q = {
        'tiles': ['3207,3408,0']
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'tiles' in data and '320734080' in data['tiles']:
            general_utils.move_and_click(data['tiles']['320734080']['x'], data['tiles']['320734080']['y'], 7, 7)
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


def click_course_start():
    q = {
        'decorativeObjects': [{
            'tile': '3221,3414,0',
            'object': '14412'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'decorativeObjects' in data and '14412' in data['decorativeObjects']:
            general_utils.move_and_click(data['decorativeObjects']['14412'][0]['x'],
                                         data['decorativeObjects']['14412'][0]['y'], 2, 2)
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
                and data['playerWorldPoint']['x'] == 3219 \
                and data['playerWorldPoint']['y'] == 3414 \
                and data['playerWorldPoint']['z'] > 0:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_1_tiles)
            break
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_course_start()
            general_utils.random_sleep(0.9, 1.1)
    # afterwards do a scan for any marks of grace


def click_step2():
    q = {
        'gameObjects': [{
            'tile': '3213,3414,3',
            'object': '14413'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14413' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14413']['x'], data['gameObjects']['14413']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break

def step2():
    click_step2()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3208 and data['playerWorldPoint']['y'] == 3414:
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
            'tile': '3200,3416,3',
            'object': '14414'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14414' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14414']['x'], data['gameObjects']['14414']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step3():
    click_step3()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3197 and data['playerWorldPoint']['y'] == 3416:
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
            'tile': '3192,3416,1',
            'object': '14832'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14832' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14832']['x'], data['gameObjects']['14832']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step4():
    click_step4()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3192 and data['playerWorldPoint']['y'] == 3406:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
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
            'tile': '3194,3401,3',
            'object': '14833'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14833' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14833']['x'], data['gameObjects']['14833']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step5():
    click_step5()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3193 and data['playerWorldPoint']['y'] == 3398:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            mark = handle_marks(mog_tiles.area_5_tiles)
            # this area is so large some marks are not in eyesight of the next obstacle click box
            if mark:
                q = {
                    'tiles': ['3200,3396,3']
                }
                data = general_utils.query_game_data(q)
                if 'tiles' in data and '320033963' in data['tiles']:
                    general_utils.move_and_click(data['tiles']['320033963']['x'], data['tiles']['320033963']['y'], 4, 5)
                    general_utils.wait_until_stationary()
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step5()


def click_step6():
    q = {
        'gameObjects': [{
            'tile': '3209,3400,3',
            'object': '14834'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14834' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14834']['x'], data['gameObjects']['14834']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step6():
    click_step6()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3218 and data['playerWorldPoint']['y'] == 3399:
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
            'tile': '3233,3402,3',
            'object': '14835'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14835' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14835']['x'], data['gameObjects']['14835']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step7():
    click_step7()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3236 and data['playerWorldPoint']['y'] == 3403:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_7_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step7()


def click_step8():
    q = {
        'gameObjects': [{
            'tile': '3237,3409,3',
            'object': '14836'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14836' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14836']['x'], data['gameObjects']['14836']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step8():
    click_step8()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['y'] == 3410:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_8_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step8()


def click_step9():
    q = {
        'gameObjects': [{
            'tile': '3236,3416,3',
            'object': '14841'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '14841' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['14841']['x'], data['gameObjects']['14841']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step9():
    click_step9()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3236 and data['playerWorldPoint']['y'] == 3417:
            general_utils.wait_until_stationary()
            break
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step9()


def look_up():
    keyboard.press('up')
    general_utils.random_sleep(1, 1.2)
    keyboard.release('up')


def main():
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 47, 54, 423, 551, 'pass_70', look_up)
        fell2 = False
        fell4 = False
        step1()
        fell2 = step2()
        if fell2 == 'fell':
            continue
        general_utils.random_sleep(0.5, 0.6)
        step3()
        fell4 = step4()
        if fell4 == 'fell':
            go_to_center()
            continue
        step5()
        step6()
        step7()
        step8()
        step9()
        general_utils.random_sleep(1, 1.2)


main()