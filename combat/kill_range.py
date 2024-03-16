import math

import pyautogui

import osrs

min_health = 12
# hillt giants
#npc_ids = ['2098', '2099', '2100', '2101', '2103']

npc_ids = ['5816']
#npc_ids = ['1153']
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
    qh.set_npcs(npc_ids)
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defense'})
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_widgets({'233,0'})
    while True:
        qh.query_backend()
        if not qh.get_interating_with():
            osrs.game.break_manager_v4(script_config)

        if qh.get_skills('hitpoints')['boostedLevel'] < min_health:
            k = qh.get_inventory(karambwan_id)
            if not k:
                exit('out of karambwans')
            osrs.move.click(k)
            osrs.clock.sleep_one_tick()
        elif qh.get_interating_with():
            print('In combat.')
        else:
            targ = find_next_target(qh.get_npcs())
            if targ:
                print(targ['health'])
                osrs.move.fast_click(targ)

        if qh.get_skills('ranged')['boostedLevel'] - qh.get_skills('ranged')['level'] < 5:
            super_combat = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), [169, 171, 173, 2444])
            if not super_combat:
                print('out of super combats')
            else:
                osrs.move.click(super_combat)

        # check if i leveled
        if qh.get_widgets('233,0'):
            for i in range(3):
                osrs.keeb.press_key('space')
                osrs.clock.sleep_one_tick()



main()