import datetime

import osrs.move as move
import osrs.item_ids as item_ids
import osrs.keeb as keeb
import osrs.queryHelper
import osrs.queryHelper as queryHelper

necklace_ids = [
    item_ids.RING_OF_DUELING8,
    item_ids.RING_OF_DUELING7,
    item_ids.RING_OF_DUELING6,
    item_ids.RING_OF_DUELING5,
    item_ids.RING_OF_DUELING4,
    item_ids.RING_OF_DUELING3,
    item_ids.RING_OF_DUELING2,
    item_ids.RING_OF_DUELING1,
]


def dueling_to_c_wars():
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


def dueling_to_ferox():
    qh = queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_chat_options()
    click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if (3121 <= qh.get_player_world_location('x') <= 3155
                    and 3611 <= qh.get_player_world_location('y') <= 3646):
            return
        elif qh.get_chat_options("ferox", fuzzy=True):
            keeb.write(str(qh.get_chat_options("ferox", fuzzy=True)))
        elif qh.get_inventory(necklace_ids) and (datetime.datetime.now() - click).total_seconds() > 10:
            move.right_click_v6(qh.get_inventory(necklace_ids), 'Rub', qh.get_canvas(), in_inv=True)
            click = datetime.datetime.now()


def house_tele(outside=False, house_loc='rimmington'):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_canvas()
    last_tele = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') > 9000:
            return
        elif 2948 <= qh.get_player_world_location('x') <= 2958 and 3216 <= qh.get_player_world_location('y') <= 3228:
            return
        elif qh.get_inventory(osrs.item_ids.TELEPORT_TO_HOUSE) and (datetime.datetime.now() - last_tele).total_seconds() > 10:
            if outside:
                osrs.move.right_click_v6(
                    qh.get_inventory(osrs.item_ids.TELEPORT_TO_HOUSE),
                    'Outside',
                    qh.get_canvas(),
                    in_inv=True
                )
            else:
                osrs.move.click(qh.get_inventory(osrs.item_ids.TELEPORT_TO_HOUSE))
            last_tele = datetime.datetime.now()


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


def tab_to_varrock():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    last_tab = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # in varrock center
        if 3195 <= qh.get_player_world_location('x') <= 3226 and 3419 <= qh.get_player_world_location(
                'y') <= 3438:
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            return
        elif qh.get_inventory(osrs.item_ids.VARROCK_TELEPORT) and (datetime.datetime.now() - last_tab).total_seconds() > 10:
            osrs.move.click(qh.get_inventory(osrs.item_ids.VARROCK_TELEPORT))
            last_tab = datetime.datetime.now()