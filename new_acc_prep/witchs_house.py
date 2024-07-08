import osrs
import util_functions
import transport_functions

quest_dialogue = [
    "What's the matter?", "Ok, I'll see what I can do.", "Yes."
]


def start():
    util_functions.talk_to_npc('boy')
    util_functions.dialogue_handler(quest_dialogue)


def search_plant():
    plant_id = 2867
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {plant_id})
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.DOOR_KEY.value):
            return
        elif qh.get_objects_v2('game', plant_id):
            osrs.move.fast_click(qh.get_objects_v2('game', plant_id)[0])


def enter_witch_house():
    door_id = 2861
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2901:
            return
        elif qh.get_objects_v2('wall', door_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id)[0])


def go_to_basement():
    door_id = 24686
    ladder_id = 24718
    inter_tile = '2904,3476,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_objects_v2('game', {ladder_id})
    qh.set_player_world_location()
    qh.set_tiles({inter_tile})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') >= 5500:
            return
        elif qh.get_player_world_location('y') <= 3474 and qh.get_objects_v2('wall', door_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id)[0])
        elif qh.get_player_world_location('y') <= 3474 and qh.get_tiles(inter_tile):
            osrs.move.fast_click(qh.get_tiles(inter_tile))
        elif (2901 <= qh.get_player_world_location('x') <= 2907
              and 3475 <= qh.get_player_world_location('y') <= 3476
              and qh.get_objects_v2('game', ladder_id)):
            osrs.move.fast_click(qh.get_objects_v2('game', ladder_id)[0])


def enter_gate_area():
    door_id = 2865
    inter_tile = '2901,9874,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') <= 2902:
            return
        elif qh.get_objects_v2('wall', door_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id)[0])
        elif qh.get_player_world_location('x') >= 2903 and qh.get_tiles(inter_tile):
            osrs.move.fast_click(qh.get_tiles(inter_tile))


def leave_gate_area():
    door_id = 2865
    inter_tile = '2904,9874,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2903:
            return
        elif qh.get_objects_v2('wall', door_id):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id)[0])
        elif qh.get_player_world_location('x') <= 2902 and qh.get_tiles(inter_tile):
            osrs.move.fast_click(qh.get_tiles(inter_tile))


def search_cupboards():
    closed_cb_id = 2868
    open_cb_id = 2869
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {closed_cb_id, open_cb_id})
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.MAGNET.value):
            return
        elif qh.get_objects_v2('game', closed_cb_id):
            osrs.move.fast_click(qh.get_objects_v2('game', closed_cb_id)[0])
        elif qh.get_objects_v2('game', open_cb_id):
            osrs.move.fast_click(qh.get_objects_v2('game', open_cb_id)[0])


def return_to_ground_floor():
    door_id = 24686
    ladder_id = 24717
    inter_tile = '2902,3469,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_objects_v2('game', {ladder_id})
    qh.set_player_world_location()
    qh.set_tiles({inter_tile})
    while True:
        qh.query_backend()
        if 2901 <= qh.get_player_world_location('x') <= 2907 and 3468 <= qh.get_player_world_location('y') <= 3474:
            return
        elif (2901 <= qh.get_player_world_location('x') <= 2907
              and 3475 <= qh.get_player_world_location('y') <= 3476
              and qh.get_objects_v2('wall', door_id, 6)):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id, 6)[0])
        elif (2901 <= qh.get_player_world_location('x') <= 2907
              and 3475 <= qh.get_player_world_location('y') <= 3476 and qh.get_tiles(inter_tile)):
            osrs.move.fast_click(qh.get_tiles(inter_tile))
        elif (qh.get_player_world_location('y') >= 5500
              and qh.get_objects_v2('game', ladder_id)):
            osrs.move.fast_click(qh.get_objects_v2('game', ladder_id)[0])


def enter_mouse_room():
    door_id = 24686
    inter_tile = '2902,3466,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_player_world_location()
    qh.set_tiles({inter_tile})
    while True:
        qh.query_backend()
        if 2901 <= qh.get_player_world_location('x') <= 2903 and 3466 <= qh.get_player_world_location('y') <= 3467:
            return
        elif (2901 <= qh.get_player_world_location('x') <= 2907 and 3468 <= qh.get_player_world_location('y') <= 3474
              and qh.get_objects_v2('wall', door_id, 3)):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id, 3)[0])
        elif 2901 <= qh.get_player_world_location('x') <= 2907 and 3468 <= qh.get_player_world_location('y') <= 3474 and qh.get_tiles(inter_tile):
            osrs.move.fast_click(qh.get_tiles(inter_tile))


def catch_mouse():
    main_chat_widget = '162,34'
    qh1 = osrs.queryHelper.QueryHelper()
    qh1.set_yaw(1536)
    qh1.query_backend()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_npcs_by_name(['mouse'])
    qh.set_canvas()
    qh.set_widgets({main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.CHEESE.value):
            res = osrs.move.right_click_v6(
                qh.get_inventory(osrs.item_ids.ItemIDs.CHEESE.value), 'Drop', qh.get_canvas(), in_inv=True
            )
            if res:
                break
    osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.MAGNET.value))
    while True:
        qh.query_backend()
        if qh.get_npcs_by_name():
            res = osrs.move.right_click_v6(
                qh.get_npcs_by_name()[0],
                'Use',
                qh.get_canvas(),
                in_inv=True
            )
            if res:
                break
    while True:
        qh.query_backend()
        if qh.get_widgets(main_chat_widget):
            break
    qh1.set_yaw(0)
    qh1.query_backend()


def enter_garden():
    door_id = 2862
    inter_tile = '2901,3464,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_player_world_location()
    qh.set_tiles({inter_tile})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') <= 3465:
            return
        elif qh.get_player_world_location('y') >= 3466 and qh.get_objects_v2('wall', door_id, 3):
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id, 3)[0])
        elif qh.get_player_world_location('y') >= 3466 and qh.get_tiles(inter_tile):
            osrs.move.fast_click(qh.get_tiles(inter_tile))


def garden_left_to_right():
    t1 = '2909,3460,0'
    t2 = '2933,3460,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs(['3995'])
    qh.set_tiles({t1, t2})
    osrs.player.toggle_run('on')
    while True:
        qh.query_backend()
        if (qh.get_player_world_location('x') <= 2908
                and qh.get_npcs() and qh.get_npcs()[0]['x_coord'] == 2904 and qh.get_npcs()[0]['y_coord'] == 3463
                and qh.get_tiles(t1)):
            osrs.clock.random_sleep(4.8, 4.9)
            osrs.move.fast_click(qh.get_tiles(t1))
        elif qh.get_player_world_location('x') >= 2907 and qh.get_npcs() and qh.get_npcs()[0]['x_coord'] <= 2908 and qh.get_tiles(t2):
            osrs.move.fast_click(qh.get_tiles(t2))
        elif qh.get_player_world_location('x') >= 2932:
            return


def garden_right_to_left():
    t1 = '2909,3460,0'
    t2 = '2933,3460,0'
    fountain_id = 2864
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs(['3995'])
    qh.set_tiles({t1, t2})
    qh.set_objects_v2('game', {fountain_id}),
    osrs.player.toggle_run('on')
    while True:
        qh.query_backend()
        if (qh.get_player_world_location('x') >= 2932
                and qh.get_npcs() and qh.get_npcs()[0]['x_coord'] == 2930 and qh.get_npcs()[0]['y_coord'] == 3463
                and qh.get_objects_v2('game', fountain_id)):
            osrs.clock.random_sleep(4, 4.1)
            osrs.move.fast_click(qh.get_objects_v2('game', fountain_id)[0])
        elif qh.get_player_world_location('y') >= 3467:
            return


def search_fountain():
    fountain_id = 2864
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_objects_v2('game', {fountain_id}),
    qh.set_widgets({util_functions.main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(util_functions.main_chat_widget):
            osrs.keeb.press_key('space')
        elif qh.get_inventory(2411):
            return
        elif qh.get_objects_v2('game', fountain_id):
            osrs.move.fast_click(qh.get_objects_v2('game', fountain_id)[0])


def fountain_to_shed_door():
    t1 = '2913,3466,0'
    t2 = '2933,3466,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_npcs(['3995'])
    qh.set_tiles({t1, t2})
    osrs.player.toggle_run('on')
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') <= 2912 and qh.get_tiles(t1):
            osrs.move.fast_click(qh.get_tiles(t1))
        elif (qh.get_player_world_location('x') <= 2914
                and qh.get_npcs() and qh.get_npcs()[0]['x_coord'] == 2904 and qh.get_npcs()[0]['y_coord'] == 3463
                and qh.get_tiles(t2)):
            while True:
                qh.query_backend()
                if qh.get_player_world_location('x') >= 2932:
                    return
                osrs.move.fast_click(qh.get_tiles(t2))


def enter_shed():
    door_id = 2863
    inter_tile = '2935,3463,0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('wall', {door_id})
    qh.set_player_world_location()
    qh.set_tiles({inter_tile})
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2934:
            return
        elif qh.get_player_world_location('x') <= 2933 and qh.get_objects_v2('wall', door_id, 7):
            osrs.move.click(qh.get_inventory(2411))
            osrs.move.fast_click(qh.get_objects_v2('wall', door_id, 7)[0])
        elif qh.get_player_world_location('x') <= 2933 and qh.get_tiles(inter_tile):
            osrs.move.fast_click(qh.get_tiles(inter_tile))


def kill_experiments():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([
        "witch's experiment",
        "witch's experiment (second form)",
        "witch's experiment (third form)",
        "witch's experiment (fourth form)"
    ])
    qh.set_skills({'prayer'})
    qh.set_interating_with()
    qh.set_active_prayers()
    qh.set_inventory()
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62'})
    seen_fourth = False
    while True:
        qh.query_backend()
        osrs.combat_utils.prayer_handler(qh, ['protect_melee'])
        osrs.combat_utils.pot_handler(qh, {})
        print('ff', qh.get_npcs_by_name())
        if seen_fourth and not qh.get_npcs_by_name():
            return
        elif qh.get_interating_with():
            if (not seen_fourth
                and (qh.get_npcs_by_name()
                     and qh.get_npcs_by_name()[0]['name'].lower() == "witch's experiment (fourth form)")):
                seen_fourth = True
        elif qh.get_npcs_by_name():
            osrs.move.fast_click(qh.get_npcs_by_name()[0])


def take_ball():
    ball_id = 366
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {ball_id})
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory(osrs.item_ids.ItemIDs.BALL.value):
            return
        elif qh.get_objects_v2('game', ball_id):
            osrs.move.fast_click(qh.get_objects_v2('game', ball_id)[0])

def main():
    start()
    transport_functions.walk_to_loc(2894, 2898, 3470, 3474, 2896, 3472)
    search_plant()
    enter_witch_house()
    go_to_basement()
    util_functions.equip_item(osrs.item_ids.ItemIDs.LEATHER_GLOVES.value)
    util_functions.equip_air_staff_and_earth_strike()
    enter_gate_area()
    search_cupboards()
    leave_gate_area()
    return_to_ground_floor()
    enter_mouse_room()
    catch_mouse()
    enter_garden()
    garden_left_to_right()
    garden_right_to_left()
    search_fountain()
    fountain_to_shed_door()
    enter_shed()
    kill_experiments()
    osrs.player.turn_off_all_prayers()
    take_ball()
    transport_functions.tab_to_fally()
    transport_functions.walk_to_loc(2940, 2948, 3449, 3454, 2948, 3451)
    transport_functions.fally_to_tav_gate()
    start()
    util_functions.dialogue_handler()
    util_functions.wait_for_quest_complete_screen()
    osrs.player.toggle_run('off')