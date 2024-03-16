import math

import pyautogui

import osrs

min_health = 35
npc_ids = ['496']
karambwan_id = '3144'
explosive = '6664'
tentacle = '12004'
trident = '11905'
dirt = '12007'


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
    qh.set_npcs(npc_ids)
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defense'})
    qh.set_inventory()
    qh.set_interating_with()
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        if qh.get_skills('hitpoints')['boostedLevel'] < min_health:
            k = qh.get_inventory(karambwan_id)
            if not k:
                exit('out of karambwans')
            osrs.move.click(k)
            osrs.clock.sleep_one_tick()
        elif qh.get_interating_with():
            print('In combat.')
        else:
            loot_items = osrs.server.get_surrounding_ground_items_any_ids(15)
            for item in [
                tentacle,
                trident,
                dirt
            ]:
                if item in loot_items:
                    osrs.move.spam_click(
                        '{},{},0'.format(loot_items[item][0]['x_coord'], loot_items[item][0]['y_coord']), 7)
            targ = find_next_target(qh.get_npcs())
            if targ:
                osrs.move.click(qh.get_inventory(explosive))
                print(targ['health'])
                osrs.move.fast_click(targ)
                osrs.clock.random_sleep(7, 7.1)



main()