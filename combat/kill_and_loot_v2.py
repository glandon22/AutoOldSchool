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
sys.argv[1]

'''
# yak SUPER COMBATS 10 20

npc_to_kill = str(sys.argv[1]).replace('_', ' ').upper() or 'YAKS'
pot = str(sys.argv[2]) or 'SUPER COMBATS'
pot_interval = int(sys.argv[3]) or 10
min_health = int(sys.argv[4]) or 12

print(npc_to_kill, pot, pot_interval, min_health)

food_ids = [
    7946, # monkfish
    3144, # karambwan
    379, # lobster
    385, # shark
]

pot_matcher = {
    "SUPER_COMBATS": [12695, 12697, 12699, 12701],
    "SUPER_STRENGTH_AND_ATTACK": [[157, 159, 161, 2440], [145, 147, 149, 2436]],
    "RANGING_POTION": [168, 171, 173, 2444],
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


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([npc_to_kill])
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence'})
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_widgets({'233,0'})
    last_pot = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if not qh.get_interating_with():
            osrs.game.break_manager_v4(script_config)

        if qh.get_skills('hitpoints')['boostedLevel'] < min_health:
            k = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), food_ids)
            if not k:
                exit('out of food')
            osrs.move.click(k)
            osrs.clock.sleep_one_tick()
        elif qh.get_interating_with():
            print('In combat.')
        else:
            targ = find_next_target(qh.get_npcs())
            if targ:
                print(targ['health'])
                osrs.move.fast_click(targ)

        if pot != 'NONE' and (datetime.datetime.now() - last_pot).total_seconds() / 60 > pot_interval:
            last_pot = datetime.datetime.now()
            if pot == "SUPER_STRENGTH_AND_ATTACK":
                str = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher[pot][0])
                atk = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher[pot][1])
                if not str:
                    print('out of str pots')
                else:
                    osrs.move.click(str)

                if not atk:
                    print('out of atk pots')
                else:
                    osrs.move.click(atk)
            else:
                selected_pot = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher[pot])
                if not selected_pot:
                    print('out of selected_pot')
                else:
                    osrs.move.click(selected_pot)

        # check if i leveled
        if qh.get_widgets('233,0'):
            for i in range(3):
                osrs.keeb.press_key('space')
                osrs.clock.sleep_one_tick()



main()