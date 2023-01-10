from osrs_utils import general_utils
monster_to_kill = 'Hill Giant'

def main():
    npc_curr_target_id = 0
    while True:
        q = {
            'interactingWith': True,
            'npcsToKill': [monster_to_kill],
        }
        data = general_utils.query_game_data(q)
        if 'interactingWith' in data and data['interactingWith'] == monster_to_kill:
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