import datetime

import osrs


def find_house():
    post_id = '29091'
    player_house_name_widget = '52,9'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects(
        {'2952,3221,0'},
        {post_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_widgets({player_house_name_widget})
    last_click = datetime.datetime.now()
    while True:
        qh.query_backend()
        # portal is up, not lets search for names
        if qh.get_widgets(player_house_name_widget):
            qh1 = osrs.queryHelper.QueryHelper()
            for i in range(1, 10):
                qh1.set_widgets({f'52,9,{i}', f'52,13,{i}'})
            qh1.query_backend()
            for i in range(1, 10):
                if qh1.get_widgets(f'52,9,{i}')['text'] != '' and qh1.get_widgets(f'52,13,{i}')['text'] == 'Y':
                    osrs.keeb.press_key('esc')
                    return qh1.get_widgets(f'52,9,{i}')['text']
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, post_id) and (
                datetime.datetime.now() - last_click).total_seconds() > 7:
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, post_id)[0])
            last_click = datetime.datetime.now()


def leave_house():
    house_portal_id = 4525
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects_v2('game', {house_portal_id})
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') < 5000:
            return
        elif qh.get_objects_v2('game', house_portal_id):
            osrs.move.fast_click(qh.get_objects_v2('game', house_portal_id)[0])


def use_bones():
    gilded_id = 13197
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects_v2('game', {gilded_id})
    while True:
        qh.query_backend()
        if not qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value) or qh.get_player_world_location('x') < 5000:
            return
        elif qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value) and qh.get_objects_v2('game', gilded_id):
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value))
            res = osrs.move.right_click_v6(qh.get_objects_v2('game', gilded_id)[0], 'Use', qh.get_canvas())


def offer_bones(house):
    chat_input_widget = '162,42'
    portal_id = '15478'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_npcs_by_name(['phials'])
    qh.set_chat_options()
    qh.set_objects(
        {'2952,3223,0'},
        {portal_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_widgets({chat_input_widget})
    last_portal_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_phials_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if (
                2944 <= qh.get_player_world_location('x') <= 2964
                and 3208 <= qh.get_player_world_location('y') <= 3232
                and not qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value + 1)
                and not qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value)
        ):
            return
        elif qh.get_chat_options():
            for i, option in enumerate(qh.get_chat_options()):
                if 'Exchange All' in option:
                    osrs.keeb.write(str(i))
                    osrs.clock.sleep_one_tick()
                    break
        elif (not qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value)
              and (datetime.datetime.now() - last_phials_click).total_seconds() > 8
              and len(qh.get_npcs_by_name()) > 0):
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value + 1))
            res = osrs.move.right_click_v6(qh.get_npcs_by_name()[0], 'Use', qh.get_canvas(), in_inv=True)
            if res:
                last_phials_click = datetime.datetime.now()
        elif (
                qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value)
                and (datetime.datetime.now() - last_portal_click).total_seconds() > 8
                and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, portal_id)
        ):
            res = osrs.move.right_click_v6(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, portal_id)[0], "Friend's house", qh.get_canvas(), in_inv=True)
            if res:
                last_portal_click = datetime.datetime.now()
        elif qh.get_widgets(chat_input_widget) and not qh.get_widgets(chat_input_widget)['isHidden']:
            osrs.keeb.write(str(house))
            osrs.clock.sleep_one_tick()
            osrs.keeb.press_key('enter')
        elif qh.get_player_world_location('x') > 7500:
            if qh.get_inventory(osrs.item_ids.ItemIDs.DRAGON_BONES.value):
                use_bones()
            else:
                leave_house()


def main():
    player_name = None
    while True:
        if not player_name:
            player_name = find_house()
        print(player_name)
        offer_bones(player_name)
        return
