import datetime
import math
import sys
import pyautogui

import osrs

'''
Arg list:
NPC to kill as string
potion to drink
how often to pot up
min health to eat at
SAFE SPOT X
SAFE SPOT Y
SAFE SPOT Z
slayer task boolean

'''
# yak SUPER COMBATS 10 20

npc_to_kill = 'jungle spider'
pot = 'SUPER_STRENGTH_AND_ATTACK'
pot_interval = 10
min_health = 12
ss_x = -1
ss_y = -1
ss_z = -1

food_ids = [
    7946,  # monkfish
    3144,  # karambwan
    379,  # lobster
    385,  # shark
]

pot_matcher = {
    "SUPER_COMBATS": [12695, 12697, 12699, 12701],
    "SUPER_STRENGTH_AND_ATTACK": [[157, 159, 161, 2440], [145, 147, 149, 2436]],
    "RANGING_POTION": [169, 171, 173, 2444],
    "MAGIC_POTION": [3040, 3042, 3044, 3046]
}

karambwan_id = '7946'


def find_next_target(npcs):
    res = False
    for npc in npcs:
        if npc['health'] != 0:
            if not res or npc['dist'] < res['dist']:
                res = npc
    return res


script_config = {
    'intensity': 'high',
    'login': False,
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def return_to_safe_spot(qh):
    if ss_x == -1 or ss_y == -1 or ss_z == -1:
        return False
    if qh.get_player_world_location('x') == ss_x and qh.get_player_world_location('y') == ss_y:
        return False
    return True


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([npc_to_kill])
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence'})
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_widgets({'233,0'})
    qh.set_tiles({f'{ss_x},{ss_y},{ss_z}'})
    qh.set_player_world_location()
    last_pot = datetime.datetime.now() - datetime.timedelta(hours=1)
    loot_handler = osrs.loot.Loot()
    while True:
        qh.query_backend()
        loot_handler.retrieve_loot()
        returning_to_safespot = return_to_safe_spot(qh)
        # confirm we are safespotting
        if returning_to_safespot:
            print('out of safespot')
            if qh.get_tiles(f'{ss_x},{ss_y},{ss_z}') and osrs.move.is_clickable(qh.get_tiles(f'{ss_x},{ss_y},{ss_z}')):
                osrs.move.fast_click_v2(qh.get_tiles(f'{ss_x},{ss_y},{ss_z}'))

        if not qh.get_interating_with():
            osrs.game.break_manager_v4(script_config)

        if qh.get_skills('hitpoints')['boostedLevel'] < min_health:
            k = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), food_ids)
            if not k:
                exit('out of food')
            osrs.move.fast_click_v2(k)
        elif qh.get_interating_with():
            print('In combat.')
        else:
            if not returning_to_safespot:
                targ = find_next_target(qh.get_npcs())
                if targ:
                    print(targ['health'])
                    osrs.move.fast_click_v2(targ)

        if pot != 'NONE' and (datetime.datetime.now() - last_pot).total_seconds() / 60 > pot_interval:
            last_pot = datetime.datetime.now()
            if pot == "SUPER_STRENGTH_AND_ATTACK":
                strpot = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher[pot][0])
                atk = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher[pot][1])
                if not strpot:
                    print('out of str pots')
                else:
                    osrs.move.fast_click_v2(strpot)

                if not atk:
                    print('out of atk pots')
                else:
                    osrs.move.fast_click_v2(atk)
            else:
                selected_pot = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher[pot])
                if not selected_pot:
                    print('out of selected_pot')
                else:
                    osrs.move.fast_click_v2(selected_pot)

        # check if i leveled
        if qh.get_widgets('233,0'):
            for i in range(5):
                osrs.keeb.press_key('space')
                osrs.clock.sleep_one_tick()
main()