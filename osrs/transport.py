import datetime

import osrs.move as move
import osrs.item_ids as item_ids
import osrs.keeb as keeb
import osrs.queryHelper as queryHelper


def dueling_to_c_wars():
    necklace_ids = [
            item_ids.ItemIDs.RING_OF_DUELING8.value,
            item_ids.ItemIDs.RING_OF_DUELING7.value,
            item_ids.ItemIDs.RING_OF_DUELING6.value,
            item_ids.ItemIDs.RING_OF_DUELING5.value,
            item_ids.ItemIDs.RING_OF_DUELING4.value,
            item_ids.ItemIDs.RING_OF_DUELING3.value,
            item_ids.ItemIDs.RING_OF_DUELING2.value,
            item_ids.ItemIDs.RING_OF_DUELING1.value,
        ]
    qh = queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_chat_options()
    click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 2434 <= qh.get_player_world_location('x') <= 2447 and 3081 <= qh.get_player_world_location('y') <= 3098:
            return
        elif qh.get_chat_options("castle wars", fuzzy=True):
            keeb.write(str(qh.get_chat_options("castle wars", fuzzy=True)))
        elif qh.get_inventory(necklace_ids) and (datetime.datetime.now() - click).total_seconds() > 10:
            move.right_click_v6(qh.get_inventory(necklace_ids), 'Rub', qh.get_canvas(), in_inv=True)
            click = datetime.datetime.now()


def walk_out_of_c_wars():
    qh = queryHelper.QueryHelper()
    qh.set_tiles({'2446,3090,0'})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') >= 2445:
            return
        elif qh.get_tiles('2446,3090,0'):
            move.fast_click(qh.get_tiles('2446,3090,0'))