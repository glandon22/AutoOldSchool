# tin 438 tin rock 11361 17 xp
# iron ore 440 rock 11364 35 xp
from osrs_utils import general_utils
import datetime
import time
import random


def main():
    ore = 440
    rock_id_to_mine = '11364'
    xp_amount = 35
    total_mined = 0
    start_time = datetime.datetime.now()
    while True:
        take_break = general_utils.break_every_hour(random.randint(37, 44), start_time)
        if take_break:
            general_utils.logout()
            break_start_time = datetime.datetime.now()
            while (datetime.datetime.now() - break_start_time).total_seconds() < random.randint(503, 694):
                time.sleep(30)
                general_utils.click_off_screen()
            start_time = datetime.datetime.now()
            general_utils.login('pass_71')
            general_utils.random_sleep(0.4, 0.5)
        q = {
            'isMining': True,
            'inv': True,
            'gameObjects': [
                {
                    'tile': '2195,2792,0',
                    'object': rock_id_to_mine
                },
                {
                    'tile': '2196,2793,0',
                    'object': rock_id_to_mine
                },
                {
                    'tile': '2197,2792,0',
                    'object': rock_id_to_mine
                }
            ]
        }
        data = general_utils.query_game_data(q)
        if data['isMining']:
            print('Total mined: ', total_mined, ' XP Gained: ', xp_amount * total_mined)
        elif not data['isMining']:
            general_utils.antiban_rest(40, 100, 150)
            if 'inv' in data:
                for item in data['inv']:
                    if item['id'] == ore:
                        general_utils.move_and_click(item['x'], item['y'], 5, 7)
                        total_mined += 1
            if 'gameObjects' in data and rock_id_to_mine in data['gameObjects']:
                general_utils.move_and_click(data['gameObjects'][rock_id_to_mine]['x'],
                                             data['gameObjects'][rock_id_to_mine]['y'], 4, 4)
                general_utils.random_sleep(0.2, 0.3)
                general_utils.click_off_screen(1800, 1850, 950, 1000, False)
                general_utils.random_sleep(0.5, 0.6)







main()

