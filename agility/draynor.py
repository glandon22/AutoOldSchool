from autoscape import general_utils
import draynor_vars as mog_tiles

# i think leveling up freezes me, may need to handle that


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
        mark = data['groundItems']['11849'][0]
        general_utils.move_and_click(mark['x'], mark['y'], 2, 3)
        general_utils.random_sleep(0.5, 0.6)
        general_utils.wait_until_stationary()
        general_utils.random_sleep(1.5, 1.6)


def click_course_start():
    q = {
        'decorativeObjects': [{
            'tile': '3103,3279,0',
            'object': '11404'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'decorativeObjects' in data and '11404' in data['decorativeObjects']:
            general_utils.move_and_click(data['decorativeObjects']['11404'][0]['x'],
                                         data['decorativeObjects']['11404'][0]['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def click_step2():
    q = {
        'groundObjects': [{
            'tile': '3098,3277,3',
            'object': '11405'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'groundObjects' in data and '11405' in data['groundObjects']:
            general_utils.move_and_click(data['groundObjects']['11405']['x'], data['groundObjects']['11405']['y'], 2, 2)
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
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3102 and data['playerWorldPoint']['y'] == 3279:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_1_tiles)
            break
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_course_start()
            general_utils.random_sleep(0.9, 1.1)
    # afterwards do a scan for any marks of grace


def step2():
    click_step2()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3090 and data['playerWorldPoint']['y'] == 3276:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_2_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step2()
    # afterwards do a scan for any marks of grace


def click_step3():
    q = {
        'groundObjects': [{
            'tile': '3092,3276,3',
            'object': '11406'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'groundObjects' in data and '11406' in data['groundObjects']:
            general_utils.move_and_click(data['groundObjects']['11406']['x'], data['groundObjects']['11406']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step3():
    click_step3()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3092 and data['playerWorldPoint']['y'] == 3266:
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
            'tile': '3089,3264,3',
            'object': '11430'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '11430' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['11430']['x'], data['gameObjects']['11430']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step4():
    click_step4()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3088 and data['playerWorldPoint']['y'] == 3261:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            handle_marks(mog_tiles.area_4_tiles)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step4()


def click_step5():
    q = {
        'gameObjects': [{
            'tile': '3088,3256,3',
            'object': '11630'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '11630' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['11630']['x'], data['gameObjects']['11630']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step5():
    click_step5()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3088 and data['playerWorldPoint']['y'] == 3255:
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
            'tile': '3095,3255,3',
            'object': '11631'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '11631' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['11631']['x'], data['gameObjects']['11631']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step6():
    click_step6()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3096 and data['playerWorldPoint']['y'] == 3256:
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
            'tile': '3102,3261,3',
            'object': '11632'
        }]
    }
    while True:
        data = general_utils.query_game_data(q)
        if 'gameObjects' in data and '11632' in data['gameObjects']:
            general_utils.move_and_click(data['gameObjects']['11632']['x'], data['gameObjects']['11632']['y'], 2, 2)
            general_utils.random_sleep(1, 1.1)
            break


def step7():
    click_step7()
    while True:
        q = {
            'playerWorldPoint': True,
        }
        data = general_utils.query_game_data(q)
        if 'playerWorldPoint' in data and data['playerWorldPoint']['x'] == 3103 and data['playerWorldPoint']['y'] == 3261:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.5, 0.6)
            break
        # i have fallen. need to restart course
        elif 'playerWorldPoint' in data and data['playerWorldPoint']['z'] == 0:
            print('i fell.')
        elif 'poseAnimation' in data and data['poseAnimation'] == 808:
            click_step7()


def main():
    while True:
        step1()
        step2()
        step3()
        step4()
        step5()
        general_utils.random_sleep(0.5, 0.6)
        step6()
        step7()

main()