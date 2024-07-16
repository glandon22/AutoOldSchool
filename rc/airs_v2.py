'''
notes

# if no ess

    # if in ferox enclave -> go to bank and get more runes
    # else -> tele to ferox enclave

# if ess
    # if in altar -> click altar
    # elif in ferox enclave -> tele to rimmington right click 'Outside'
    # else -> run near that altar

'''
import datetime

import osrs

duelings = [
    osrs.item_ids.ItemIDs.RING_OF_DUELING8.value,
    osrs.item_ids.ItemIDs.RING_OF_DUELING7.value,
    osrs.item_ids.ItemIDs.RING_OF_DUELING6.value,
    osrs.item_ids.ItemIDs.RING_OF_DUELING5.value,
    osrs.item_ids.ItemIDs.RING_OF_DUELING4.value,
    osrs.item_ids.ItemIDs.RING_OF_DUELING3.value,
    osrs.item_ids.ItemIDs.RING_OF_DUELING2.value,
    osrs.item_ids.ItemIDs.RING_OF_DUELING1.value,
]


def main(goal_level=99):
    altar = 34760
    altar_entrance = 34813
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_skills({'runecraft'})
    qh.set_canvas()
    qh.set_objects_v2('game', {altar, altar_entrance})
    last_banked = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_tele = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_dueling = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        osrs.player.toggle_run('on')
        if not qh.get_inventory(osrs.item_ids.ItemIDs.PURE_ESSENCE.value):
            # in ferox enclave
            if (3121 <= qh.get_player_world_location('x') <= 3155
                and 3611 <= qh.get_player_world_location('y') <= 3646) and \
                    (datetime.datetime.now() - last_banked).total_seconds() > 2:
                if qh.get_skills('runecraft') and qh.get_skills('runecraft')['level'] >= goal_level:
                    return
                osrs.move.go_to_loc(3135, 3631)
                osrs.clock.random_sleep(1, 1.2)
                items_to_withdraw = [
                    {'id': osrs.item_ids.ItemIDs.PURE_ESSENCE.value, 'quantity': 'All'}
                ]
                if not qh.get_inventory(duelings):
                    items_to_withdraw = [{'id': duelings, 'quantity': 1}] + items_to_withdraw
                # need to think about whether or not i want to set the withdraw quantity and how
                osrs.bank.banking_handler({
                    'deposit': [
                        {'id': osrs.item_ids.ItemIDs.AIR_RUNE.value, 'quantity': 'all'}
                    ],
                    'withdraw': [{'items': items_to_withdraw}]
                })
                last_banked = datetime.datetime.now()
                osrs.move.interact_with_object(26645, 'y', 4500, True)
            elif (datetime.datetime.now() - last_dueling).total_seconds() > 10:
                osrs.transport.dueling_to_ferox()
                last_dueling = datetime.datetime.now()
        else:
            if 3264 <= qh.get_player_world_location('x') <= 3390 and qh.get_player_world_location('y') >= 4500:
                if (datetime.datetime.now() - last_tele).total_seconds() > 15:
                    success = osrs.move.right_click_v6(
                        qh.get_inventory(osrs.item_ids.ItemIDs.TELEPORT_TO_HOUSE.value),
                        'Outside',
                        qh.get_canvas(),
                        in_inv=True
                    )
                    if success:
                        last_tele = datetime.datetime.now()
            elif qh.get_objects_v2('game', altar):
                osrs.move.fast_click(qh.get_objects_v2('game', altar)[0])
            elif qh.get_objects_v2('game', altar_entrance):
                osrs.move.fast_click(qh.get_objects_v2('game', altar_entrance)[0])
            elif (2931 <= qh.get_player_world_location('x') <= 3016
                  and 3199 <= qh.get_player_world_location('y') <= 3308):
                osrs.move.go_to_loc(2983, 3288)


