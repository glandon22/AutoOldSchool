from osrs_utils import general_utils
import keyboard


def start():
    q = {
        'npcsID': ['815']
    }
    data = general_utils.query_game_data(q)
    if 'npcs' in data:
        closest = general_utils.find_closest_target(data['npcs'])
        general_utils.move_and_click(closest['x'], closest['y'], 8, 8)
        general_utils.random_sleep(0.5, 0.8)
    keyboard.press('space')
    while True:
        q = {
            'chatOptions': True
        }
        data = general_utils.query_game_data(q)
        if 'chatOptions' in data:
            keyboard.release('space')
            general_utils.random_sleep(1.5, 1.6)
            keyboard.send('1')
            break
    general_utils.random_sleep(1.5, 1.6)
    keyboard.press('space')
    while True:
        q = {
            'chatOptions': True
        }
        data = general_utils.query_game_data(q)
        if 'chatOptions' in data:
            keyboard.release('space')
            general_utils.random_sleep(1.5, 1.6)
            keyboard.send('1')
            break


def main():
    start()


main()
