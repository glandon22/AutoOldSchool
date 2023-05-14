import datetime

from autoscape import general_utils
from pynput.keyboard import Key, Controller

keyboard = Controller()
monster_to_kill = 'Yak'
minimum_eat_health = 35
food_to_eat = [7946, 379, 361]
port = '56799'

def main():
    npc_curr_target_id = 0
    start_time = datetime.datetime.now()
    pot_time = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        start_time = general_utils.break_manager(start_time, 53, 59, 423, 551, 'pass_70', False)
        q = {
            'interactingWith': True,
            'npcsToKill': [monster_to_kill],
            'skills': ['hitpoints'],
            'inv': True
        }
        data = general_utils.query_game_data(q)
        if 'skills' in data and \
                'hitpoints' in data['skills'] and \
                data['skills']['hitpoints']['boostedLevel'] < minimum_eat_health:
            food = general_utils.are_items_in_inventory(data['inv'], food_to_eat)
            if not food:
                return print('out of food')
            general_utils.move_and_click(food[0], food[1], 4, 4)
            general_utils.random_sleep(1, 1.1)
        elif (datetime.datetime.now() - pot_time).total_seconds() > 900 and 'inv' in data:
            print('Potting up.')
            super_combat = general_utils.are_items_in_inventory_v2(data['inv'], [12695, 12697, 12699, 12701])
            if not super_combat:
                print('out of super combats')
            else:
                general_utils.move_and_click(super_combat['x'], super_combat['y'], 4, 4)
                general_utils.click_off_screen(300, 1000, 300, 700, False)
            pot_time = datetime.datetime.now()
            general_utils.random_sleep(0.5, 0.6)
        elif general_utils.have_leveled_up(port):
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        elif 'interactingWith' in data and data['interactingWith'] == monster_to_kill:
            print('In combat, no action needed.')
            general_utils.random_sleep(0.5, 0.6)
        else:
            # sleep for a sec to find a new monster
            q = {
                'npcsToKill': [monster_to_kill],
            }
            data = general_utils.query_game_data(q)
            closest = general_utils.find_closest_npc(data['npcs'], npc_curr_target_id)
            general_utils.move_and_click(closest['x'], closest['y'], 2, 2)
            npc_curr_target_id = closest['id']
            general_utils.random_sleep(3, 4)

main()