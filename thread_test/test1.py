# 2134,9305,0
import time
from datetime import datetime

import pyautogui
import osrs

'''time.sleep(0.5)
qh = osrs.queryHelper.QueryHelper()
qh.set_widgets({'161,96', '161,97'})
qh.query_backend()
print(osrs.util.combine_objects(qh.get_widgets()))'''
'''def exx():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 3145 <= qh.get_player_world_location('x') <= 3180:
        osrs.keeb.press_key('esc')
        return True


def pre():
    #osrs.keeb.press_key('f6')
    print('test')

osrs.move.interact_with_widget_v3(
    osrs.widget_ids.varrock_tele_widget_id,
    right_click_option='Grand Exchange',
    custom_exit_function=exx,
    pre_interact=pre
)'''
'''def pre():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'3372,11492,0'})
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_tiles('3372,11492,0') and qh.get_player_world_location('x') == 3374 and qh.get_player_world_location('y') == 11491:
        osrs.move.fast_click_v2(qh.get_tiles('3372,11492,0'))'''
'''osrs.move.interact_with_object_v3(
        44776,
        custom_exit_function=lambda start: (datetime.now() - start).total_seconds() > 9,
        custom_exit_function_arg=datetime.now(),
    #pre_interact=pre
    )'''

'''qh = osrs.queryHelper.QueryHelper()
qh.set_widgets({'161,35', '161,34'})
qh.query_backend()
print(qh.get_widgets())'''

'''osrs.move.go_to_loc(3209, 3433, exact_tile=True, exit_on_dest=True)
osrs.move.go_to_loc(3164, 3474, exact_tile=True, exit_on_dest=True)
osrs.move.go_to_loc(3209, 3433, exact_tile=True, exit_on_dest=True)'''
#osrs.game.buy_item_from_shop([{'id': osrs.item_ids.AIR_RUNE, 'quantity': 2, 'increment': 5}])


'''qh = osrs.queryHelper.QueryHelper()
qh.set_npcs(['3019'])
qh.set_right_click_menu()
qh.set_player_world_location()
qh.set_detailed_interating_with()
while True:
    qh.query_backend()
    closest_spider = osrs.util.find_closest_target_in_game(qh.get_npcs(), qh.get_player_world_location(), lambda npc: npc['health'] != 0)
    print(closest_spider)
    if not closest_spider:
        print('done')
        exit(77)
    elif qh.get_detailed_interating_with() and qh.get_detailed_interating_with()['health'] != 0:
        continue
    elif (qh.get_right_click_menu()
          and qh.get_right_click_menu()['entries']
          and qh.get_right_click_menu()['entries'][-1][0] == 'Attack'
          and 'Spider' in qh.get_right_click_menu()['entries'][-1][2]):
        pyautogui.click()
    elif closest_spider:
        osrs.move.instant_move(closest_spider)'''



'''qh = osrs.queryHelper.QueryHelper()
qh.set_npcs(['2854'])
qh.set_right_click_menu()
qh.set_canvas()
while True:
    qh.query_backend()
    if qh.get_npcs():
        osrs.move.right_click_v8(
            qh.get_npcs()[0],
            'Attack',
            qh,
            tg='Rat'
        )
    print(qh.get_right_click_menu())
qh = osrs.queryHelper.QueryHelper()
qh.set_inventory()
qh.set_canvas()
qh.query_backend()
osrs.move.right_click_v7(
    qh.get_inventory(osrs.item_ids.ZOMBIE_AXE),
    'Wield',
    qh.get_canvas()
)'''
'''while True:
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['Sister Senga'])
    qh.set_right_click_menu()
    qh.query_backend()
    print(qh.get_right_click_menu())'''

'''
qh = osrs.qh_v2.QueryHelper()
chat_lines = set()
for i in range(0, 50):
    chat_lines.add(f"162,56,{i * 4}")
qh.set_widgets(chat_lines)
qh.set_widgets({'162,56,0'})
# leaving this empty matches all npcs which i can filter later
qh.set_npcs([])
qh.set_objects_v2('graphics', {1767}, dist=8)
qh.set_objects_v2('game', {37738, 37739, 37743, 37744, 37745})
qh.set_varbits(['10151'])
qh.set_player_world_location()
qh.set_inventory()
qh.set_canvas()
qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62', osrs.widget_ids.run_energy_widget_id, '541,25'})
# Pillar overlay
qh.set_widgets({'413,1', '413,6', '413,7', '413,8', '413,9', '413,15', '413,21', '413,27'})
qh.set_active_prayers()
qh.set_interating_with()
qh.set_equipment()
qh.set_canvas()
qh.set_right_click_menu()
qh.set_var_player(['101'])
iters = 0
time1 = 0.0
max1 = 0
min1 = 9.0
while iters <= 1000:
    start = datetime.datetime.now()
    qh.query_backend()
    val = (datetime.datetime.now() - start).total_seconds()
    time1 += val
    iters += 1
    max1 = max(val, max1)
    min1 = min(val, min1)
    print('////////')
    print('avg: ', time1 / iters)
    print('min: ', min1)
    print('max: ', max1)
    print('////////')
'''
qh = osrs.qh_v2.QueryHelper()
chat_lines = set()
for i in range(0, 50):
    chat_lines.add(f"162,56,{i * 4}")
qh.set_widgets(chat_lines)
qh.set_widgets({'162,56,0'})
# leaving this empty matches all npcs which i can filter later
qh.set_npcs([])
qh.set_objects_v2('graphics', {1767}, dist=8)
qh.set_objects_v2('game', {37738, 37739, 37743, 37744, 37745})
qh.set_varbits(['10151'])
qh.set_player_world_location()
qh.set_inventory()
qh.set_canvas()
qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62', osrs.widget_ids.run_energy_widget_id, '541,25'})
# Pillar overlay
qh.set_widgets({'413,1', '413,6', '413,7', '413,8', '413,9', '413,15', '413,21', '413,27'})
qh.set_active_prayers()
qh.set_interating_with()
qh.set_equipment()
qh.set_canvas()
qh.set_right_click_menu()
qh.set_var_player(['101'])


osrs.combat_utils.prayer_handler(qh, ['protect_range'], cached_locations=True)
osrs.combat_utils.prayer_handler(qh, ['protect_mage'], cached_locations=True)