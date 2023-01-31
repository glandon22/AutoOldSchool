import datetime

from osrs_utils import general_utils

monster_to_kill = 'Hill Giant'
minimum_eat_health = 35
food_to_eat = [7946, 379, 361]

def main():
    npc_curr_target_id = 0
    start_time = datetime.datetime.now()
    while True:
        start_time = general_utils.break_manager(start_time, 53, 59, 423, 551, 'pass_71', False)
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