from tokenize import Triple

import osrs
from osrs.item_ids import ACORN

'''
notes
luanr isle portal id 28339

tele home
drink restore pool
lunar isle portal
bank
talk to sirsal banker and get deported
run to 2640,3687,0
click torfinn - in ungael 2277,4034,0
run to 2272,4048,0
click 31990 then in instance break
toggle run off
drink divine then drink antifire
kill
toggle run on
start again!
'''

trip_supplies = [
    {
        'id': [
            osrs.item_ids.DIAMOND_DRAGON_BOLTS_E
        ],
        'quantity': 'All'
    },
    osrs.item_ids.SUPER_RESTORE4,
    osrs.item_ids.SUPER_RESTORE4,
    osrs.item_ids.SUPER_RESTORE4,
    osrs.item_ids.DIVINE_RANGING_POTION4,
    osrs.item_ids.EXTENDED_ANTIVENOM4,
    osrs.item_ids.EXTENDED_SUPER_ANTIFIRE4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.SLAYERS_STAFF,
    {
        'id': [
            osrs.item_ids.COOKED_KARAMBWAN
        ],
        'quantity': 'All'
    },
]


def in_lunar_isle():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 2058 <= qh.get_player_world_location('x') <= 2120 and 3845 <= qh.get_player_world_location('y') <= 3953:
        return True


def in_ungael():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 2238 <= qh.get_player_world_location('x') <= 2304 and 4032 <= qh.get_player_world_location('y') <= 4098:
        return True


def in_instance():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_player_world_location('x') >= 3967:
        return True


def determine_anchor():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {31822})
    while True:
        qh.query_backend()
        print(qh.get_objects_v2('game'))
        if qh.get_objects_v2('game'):
            anchor = qh.get_objects_v2('game')[0]
            return {
                'left': {'x': anchor['x_coord'] - 2, 'y': anchor['y_coord'] + 2},
                'middle': {'x': anchor['x_coord'], 'y': anchor['y_coord'] + 2},
                'right': {'x': anchor['x_coord'] + 2, 'y': anchor['y_coord'] + 2}
            }


def wake_vork():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([8059, 8058, 8061])
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        print(qh.get_npcs())
        # vorkath is awake or waking up
        if osrs.util.find_closest_target_in_game(
                qh.get_npcs(), qh.get_player_world_location(), lambda npc: npc['id'] == 8061 or npc['id'] == 8058
        ):
            return
        elif osrs.util.find_closest_target_in_game(
                qh.get_npcs(), qh.get_player_world_location(), lambda npc: npc['id'] == 8059
        ):
            osrs.move.fast_click_v2(
                osrs.util.find_closest_target_in_game(qh.get_npcs(), qh.get_player_world_location(), lambda npc: npc['id'] == 8059)
            )


def kill_vork(anchor):
    acid_pool_id = 32000
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([8059, 8061, 8063])
    qh.set_projectiles()
    qh.set_widgets({'160,21'})
    qh.set_interating_with()
    qh.set_widgets({
        osrs.widget_ids.prayer_orb_widget_id
    })
    qh.set_inventory()
    qh.set_skills({'hitpoints', 'prayer', 'ranged'})
    qh.set_player_world_location()
    qh.set_varbit('6101')
    qh.set_objects_v2('game', {acid_pool_id})

    while True:
        qh.query_backend()

        osrs.combat_utils.fast_food_handler(qh, 35)
        osrs.combat_utils.turn_on_quick_prayers(qh)
        if list(filter(lambda proj: proj['id'] == 1481, qh.get_projectiles_v2())):
            osrs.dev.logger.warn('Fireball incoming!')
            # add function to walk to the closest safe tile

'''osrs.player.toggle_run('on')
osrs.game.tele_home_v2()
osrs.game.click_restore_pool()
osrs.move.interact_with_object_v3(
    29339, custom_exit_function=in_lunar_isle, obj_dist=25, right_click_option='Enter',
    timeout=9
)
osrs.bank.banking_handler({
    'dump_inv': True,
    'withdraw_v2': trip_supplies
})
osrs.game.talk_to_npc('sirsal banker', right_click=True)
osrs.game.dialogue_handler([], 1)
osrs.move.go_to_loc(2640, 3687)
osrs.game.talk_to_npc('torfinn', custom_exit=in_ungael)
osrs.move.go_to_loc(2272, 4048)
osrs.move.interact_with_object_v3(
    31990, custom_exit_function=in_instance
)
osrs.player.toggle_run('off')'''
wake_vork()
kill_vork(determine_anchor())