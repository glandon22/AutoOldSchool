
import osrs
import keyboard


def start():
    q = {
        'npcsID': ['815']
    }
    data = osrs.server.query_game_data(q)
    if 'npcs' in data:
        closest = osrs.util.find_closest_target(data['npcs'])
        osrs.move.move_and_click(closest['x'], closest['y'], 8, 8)
        osrs.clock.random_sleep(0.5, 0.8)
    keyboard.press('space')
    while True:
        q = {
            'chatOptions': True
        }
        data = osrs.server.query_game_data(q)
        if 'chatOptions' in data:
            keyboard.release('space')
            osrs.clock.random_sleep(1.5, 1.6)
            keyboard.send('1')
            break
    osrs.clock.random_sleep(1.5, 1.6)
    keyboard.press('space')
    while True:
        q = {
            'chatOptions': True
        }
        data = osrs.server.query_game_data(q)
        if 'chatOptions' in data:
            keyboard.release('space')
            osrs.clock.random_sleep(1.5, 1.6)
            keyboard.send('1')
            break


def main():
    start()


main()
