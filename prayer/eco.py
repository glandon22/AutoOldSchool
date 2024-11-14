import datetime

import osrs.move

bone = osrs.item_ids.DRAGON_BONEMEAL
bone_to_process = osrs.item_ids.DRAGON_BONES
# slime

def click_bucket():
    qh = osrs.qh_v2.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(osrs.item_ids.BUCKET):
        osrs.move.fast_click_v2(qh.get_inventory(osrs.item_ids.BUCKET))


def get_slime():
    osrs.move.interact_with_object_v3(
        17119,
        obj_type='ground',
        custom_exit_function=osrs.inv.not_in_inv_check,
        custom_exit_function_arg=osrs.item_ids.BUCKET,
        pre_interact=click_bucket
    )


def offer_bones():
    qh = osrs.qh_v2.QueryHelper()
    qh.set_inventory()
    qh.set_objects_v2('game', {16654})
    qh.set_player_animation()
    started = False
    last = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if not qh.get_inventory(bone_to_process):
            break
        if qh.get_player_animation() == 1649 and not started:
            started = True
        elif qh.get_objects_v2('game', 16654) and (datetime.datetime.now() - last).total_seconds() > 5:
            osrs.move.fast_click_v2(qh.get_inventory(bone_to_process))
            osrs.move.fast_click(qh.get_objects_v2('game', 16654)[0])
            last = datetime.datetime.now()

    osrs.move.interact_with_object_v3(
        16647,
        coord_type='z',
        coord_value=0,
        greater_than=False
    )
    osrs.move.interact_with_object_v3(
        16648,
        custom_exit_function=osrs.inv.not_in_inv_check,
        custom_exit_function_arg=bone,
        timeout=1
    )

offer_bones()