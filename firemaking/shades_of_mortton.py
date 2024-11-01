''''
notes

171,5 repair state
171,7 resources
171,9 sanctity

game obj 4078 wall to reinforce

limestone brick shop item widget 300,16,2
timber beam 300,16,3
swamp paste 300,16,4


to buy resources:
run to 3485, 3293
go into store on tile 3488, 3297, open door 1535 on tile 3488,3294,0
'''
from datetime import datetime, timedelta

import osrs

def transform_owner():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['1289'])
    qh.query_backend()
    if qh.get_npcs():
        osrs.move.fast_click_v2(qh.get_npcs()[0])

def in_store():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    return osrs.util.is_point_in_rectangle(
        qh.get_player_world_location('x'),
        qh.get_player_world_location('y'),
        3487, 3295, 3490, 3297
    )


def buy_supplies():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()

    osrs.move.go_to_loc(3484, 3294)
    osrs.move.interact_with_object_v3(
        1535,
        custom_exit_function=in_store,
        right_click_option='Open',
        obj_tile={'x': 3488, 'y': 3294, 'z': 0},
        intermediate_tile='3489,3295,0',
        obj_type='wall'
    )
    osrs.move.interact_with_npc(
        ['1289', '1290'],
        exit_on_interact=True,
        timeout=3,
    )
    osrs.game.dialogue_handler(['Can I see the building store please?'])
    osrs.game.buy_item_from_shop([
        {'id': osrs.item_ids.TIMBER_BEAM, 'quantity': 5, 'increment': 5},
        {'id': osrs.item_ids.LIMESTONE_BRICK, 'quantity': 5, 'increment': 5},
        {'id': osrs.item_ids.SWAMP_PASTE, 'quantity': 50, 'increment': 50}
    ])
    osrs.move.interact_with_npc(
        ['1289', '1290'],
        exit_on_interact=True,
        timeout=3,
    )
    osrs.game.dialogue_handler(['Can I see the general store please?'])
    osrs.game.buy_item_from_shop([
        {'id': osrs.item_ids.OLIVE_OIL4, 'quantity': 1, 'increment': 50},
    ])
    osrs.move.interact_with_object_v3(
        1535,
        coord_type='y',
        coord_value=3294,
        right_click_option='Open',
        obj_tile={'x': 3488, 'y': 3290, 'z': 0},
        intermediate_tile='3488,3289,0',
        obj_type='wall',
        greater_than=False,
    )
    osrs.move.go_to_loc(3506, 3311)


def restore_temple():
    repair = '171,5'
    resources = '171,7'
    sanctity = '171,9'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_animation()
    qh.set_inventory()
    qh.set_widgets({repair, resources, sanctity})
    qh.set_objects_v2('game', {4078})
    last_fixing = datetime.now() - timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(sanctity) and int(qh.get_widgets(sanctity)['text'][:-1]) >= 100:
            return osrs.dev.logger.info("Achieved fulled sanctity while rebuilding temple.")
        elif qh.get_widgets(resources) and qh.get_widgets(resources)['text'][:-1] == '0':
            return osrs.dev.logger.warning("Ran out of materials while rebuilding temple.")
        elif (qh.get_player_animation() != 832
              and (datetime.now() - last_fixing).total_seconds() > 3.0
              and qh.get_objects_v2('game', 4078)):
            osrs.move.fast_click_v2(qh.get_objects_v2('game', 4078)[0])
        elif qh.get_player_animation() == 832:
            last_fixing = datetime.now()


def bless_oil():
    sanctity = '171,9'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_animation()
    qh.set_inventory()
    qh.set_widgets({sanctity})
    qh.set_objects_v2('game', {4090})
    last_fixing = datetime.now() - timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(sanctity) and int(qh.get_widgets(sanctity)['text'][:-1]) < 10:
            return osrs.dev.logger.info("Sanctity depleted while blessing oil.")
        elif not qh.get_inventory(osrs.item_ids.OLIVE_OIL4):
            return osrs.dev.logger.info("Finished blessing olive oil.")
        elif (qh.get_player_animation() != 832
              and (datetime.now() - last_fixing).total_seconds() > 3.0
              and qh.get_objects_v2('game', 4090)):
            osrs.move.fast_click_v2(qh.get_objects_v2('game', 4090)[0])
        elif qh.get_player_animation() == 832:
            last_fixing = datetime.now()


def main():
    repair = '171,5'
    resources = '171,7'
    sanctity = '171,9'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_animation()
    qh.set_inventory()
    qh.set_widgets({repair, resources, sanctity})
    while True:
        buy_supplies()
        restore_temple()
        osrs.move.go_to_loc(3506, 3311)
        bless_oil()


main()