import math

import pyautogui

import osrs

min_health = 35
npc_ids = ['2098', '2099', '2100', '2101', '2103']
karambwan_id = '3144'

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
    qh.set_game_state()
    qh.set_canvas()
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        if qh.get_skills('attack')['boostedLevel'] >= 92:
            exit('73 atk reached')
        if qh.get_skills('hitpoints')['boostedLevel'] < min_health:
            k = qh.get_inventory(karambwan_id)
            if not k:
                exit('out of karambwans')
            osrs.move.click(k)
            osrs.clock.sleep_one_tick()
        elif qh.get_interating_with():
            #print('In combat.')
            a = 1
        else:
            targ = find_next_target(qh.get_npcs())
            if targ:
                print(targ['health'])
                osrs.move.fast_click(targ)



main()