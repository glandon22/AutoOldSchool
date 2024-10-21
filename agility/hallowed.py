import math
from datetime import datetime
from math import floor

import osrs

first_floor_only = False
second_floor_only = True


def get_prev_inv(item):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    return osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), item)


def is_point_in_rectangle(x, y, x1, y1, x2, y2):
    return x1 <= x <= x2 and y1 <= y <= y2


def find_second_floor_anchor(target, base_loc, obj_type='ground'):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2(obj_type, {target})
    while True:
        qh.query_backend()
        if qh.get_objects_v2(obj_type, target):
            return {
                'x': qh.get_objects_v2(obj_type, target)[0]['x_coord'] - base_loc['x'],
                'y': qh.get_objects_v2(obj_type, target)[0]['y_coord'] - base_loc['y'],
            }


def find_floor_anchor_with_player_loc(base_loc, expected_z):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('z') == expected_z:
            return {
                'x': qh.get_player_world_location('x') - base_loc['x'],
                'y': qh.get_player_world_location('y') - base_loc['y'],
            }


def in_coords(qh: osrs.queryHelper.QueryHelper, dest):
    return (dest['x_min'] <= qh.get_player_world_location('x') <= dest['x_max']
            and dest['y_min'] <= qh.get_player_world_location('y') <= dest['y_max'])


def on_tomb_anchor():
    qh1 = osrs.queryHelper.QueryHelper()
    qh1.set_player_world_location()
    qh1.set_objects_v2('game', {38451})
    qh1.query_backend()
    tomb = qh1.get_objects_v2('game', 38451, dist=4)
    if tomb:
        tomb = osrs.util.find_closest_target_in_game(
            tomb,
            qh1.get_player_world_location(),
            lambda obj: obj['x_coord'] == qh1.get_player_world_location('x')
        )
        if tomb:
            return True


def pass_sword(sword_loc, steps: list, dest, sword_thrower_id, on_npc_position=False):
    osrs.dev.logger.info("Handling a sword obstacle")
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['9669'])
    qh.set_objects_v2('game', {sword_thrower_id})
    qh.set_player_world_location()
    qh.set_tiles({
        f"{steps[0][0]},{steps[0][1]},{steps[0][2]}"
    })

    while True:
        qh.query_backend()
        if in_coords(qh, dest):
            osrs.dev.logger.info("Successfully passed a sword obstacle")
            return

        thrower = qh.get_objects_v2('game', sword_thrower_id) if not on_npc_position else qh.get_npcs()
        if thrower:
            thrower = osrs.util.find_closest_target_in_game(
                thrower,
                qh.get_player_world_location(),
                lambda obj: obj['x_coord'] == sword_loc['x']
                            and obj['y_coord'] == sword_loc['y']
                            and (
                                    (
                                            on_npc_position
                                            and qh.get_objects_v2('game', sword_thrower_id)
                                            and qh.get_objects_v2('game', sword_thrower_id)[0]['animation'] == 8669
                                    )
                                    or obj['animation'] == 8670
                            )
            )
        if thrower:
            osrs.dev.logger.info("Sword obstacle is safe to pass - running to destination")
            for step in steps:
                osrs.move.go_to_loc(*step, skip_dax=True, player_loc=qh.get_player_world_location())
        elif qh.get_tiles(f"{steps[0][0]},{steps[0][1]},{steps[0][2]}"):
            osrs.dev.logger.info("Sword is blocking path - pre-hovering next tile click")
            osrs.move.fast_move(qh.get_tiles(f"{steps[0][0]},{steps[0][1]},{steps[0][2]}"))


def inv_changed(prev):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    return not osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.HALLOWED_MARK) == prev


def inv_changed_v2(args):
    prev = args[0]
    item = args[1]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    return not osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), item) == prev


def pass_flames(qh: osrs.queryHelper.QueryHelper or None, steps: list, anchor: dict):
    if qh is None:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_player_world_location()
        qh.set_objects_v2('game', set([item['obj_id'] for item in steps]))
    for idx, step in enumerate(steps):
        formatted_dest_tile = f"{step['dest_x'] + anchor['x']},{step['dest_y'] + anchor['y']},{step['dest_z']}"
        qh.set_tiles({
            formatted_dest_tile
        })
        while True:
            qh.query_backend()
            if qh.get_player_world_location(step['coord_type']) == anchor[step['coord_type']] + step['coord_val']:
                break
            while True:
                qh.query_backend()
                if qh.get_objects_v2('game', step['obj_id']) \
                        and qh.get_objects_v2('game', step['obj_id'])[0]['animation'] in [8659] \
                        and qh.get_tiles(formatted_dest_tile):
                    break
            osrs.move.fast_click_v2(qh.get_tiles(formatted_dest_tile))
            start_time = datetime.now()
            while True:
                qh.query_backend()
                if (datetime.now() - start_time).total_seconds() > 5:
                    osrs.dev.logger.warning("Timed out waiting to arrive on step in flame obstacle")
                    break
                elif qh.get_player_world_location('x') == step['dest_x'] + anchor['x'] and \
                        qh.get_player_world_location('y') == step['dest_y'] + anchor['y']:
                    osrs.dev.logger.info("Successfully made it to step in flame obstacle")
                    break


def floor_1_scenario_1(anchor):
    def calc_anchor_tomb(step):
        return {
            'x': step['x_coord'] - 2265,
            'y': step['y_coord'] - 5984
        }

    anchor_vase_id = 38484
    sword_thrower_id = 38438
    flame_shooter_1_id = 38412
    flame_shooter_2_id = 38409
    floor_exit_id = 38464
    arrow_shooter_id = 38444
    step_to_floor_2 = 38456
    blue_arrow_projectile_npc_id = '9672'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects_v2(
        'game', {
            anchor_vase_id, sword_thrower_id, flame_shooter_1_id, flame_shooter_2_id, floor_exit_id, arrow_shooter_id
        }
    )
    qh.set_objects_v2(
        'ground', {step_to_floor_2}
    )
    qh.set_npcs([blue_arrow_projectile_npc_id])
    qh.set_inventory()
    osrs.dev.logger.info("Running to start of sword obstacle")
    osrs.move.go_to_loc(2280 + anchor['x'], 5955 + anchor['y'], 2, exact_tile=True, skip_dax=True)
    while True:
        qh.query_backend()
        if qh.get_objects_v2('game', sword_thrower_id) \
                and qh.get_objects_v2('game', sword_thrower_id)[0]['animation'] in [-1, 8670]:
            osrs.dev.logger.info("Running through sword obstacle")
            break
    osrs.move.go_to_loc(2272 + anchor['x'], 5953 + anchor['y'], 2, skip_dax=True)
    osrs.move.go_to_loc(2262 + anchor['x'], 5957 + anchor['y'], 2, skip_dax=True)
    osrs.dev.logger.info("Past the sword obstacle")
    osrs.move.go_to_loc(2272 + anchor['x'], 5961 + anchor['y'], 2, exact_tile=True, skip_dax=True)
    flames_step_1 = {
        'coord_type': 'y', 'coord_val': 5966, 'obj_id': flame_shooter_1_id,
        'dest_x': 2272, 'dest_y': 5966, 'dest_z': 2,
    }
    flames_step_2 = {
        'coord_type': 'y', 'coord_val': 5970, 'obj_id': flame_shooter_1_id,
        'dest_x': 2272, 'dest_y': 5970, 'dest_z': 2,
    }
    flames_step_3 = {
        'coord_type': 'y', 'coord_val': 5973, 'obj_id': flame_shooter_2_id,
        'dest_x': 2272, 'dest_y': 5973, 'dest_z': 2,
    }
    pass_flames(qh, [flames_step_1, flames_step_2, flames_step_3], anchor)
    qh.set_tiles({
        f"{2263 + anchor['x']},{5982 + anchor['y']},2"
    })
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') >= 5980 + anchor['y']:
            break
        while True:
            qh.query_backend()
            blue_arrow = qh.get_objects_v2('game', arrow_shooter_id)
            if blue_arrow:
                blue_arrow = osrs.util.find_closest_target_in_game(
                    blue_arrow, qh.get_player_world_location(),
                    lambda npc: npc['y_coord'] - anchor['y'] in [5976, 5977] and npc['animation'] in [8682, 8683]
                )
            if qh.get_player_world_location('y') >= 5979 + anchor['y']:
                break
            elif blue_arrow and qh.get_tiles(f"{2263 + anchor['x']},{5982 + anchor['y']},2"):
                osrs.move.fast_click_v2(qh.get_tiles(f"{2263 + anchor['x']},{5982 + anchor['y']},2"))
                break
    osrs.move.interact_with_object_v3(
        floor_exit_id,
        coord_type='z',
        coord_value=1,
        greater_than=False
    )
    while True:
        qh.query_backend()
        if qh.get_objects_v2('ground', step_to_floor_2):
            break
    tomb_anchor = calc_anchor_tomb(qh.get_objects_v2('ground', step_to_floor_2)[0])
    osrs.move.interact_with_object_v3(
        39527,
        coord_type='y',
        coord_value=5984 + tomb_anchor['y'] - 5,
        obj_type='ground',
        greater_than=False
    )
    qh.query_backend()
    prev_inv = osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.HALLOWED_MARK)
    osrs.move.interact_with_object_v3(
        39544,
        custom_exit_function=inv_changed,
        custom_exit_function_arg=prev_inv
    )
    osrs.move.interact_with_object_v3(
        39527,
        coord_type='y',
        coord_value=5984 + tomb_anchor['y'] - 7,
        obj_type='ground',
        greater_than=True,
        obj_tile={'x': 2265 + tomb_anchor['x'] - 3, 'y': 5984 + tomb_anchor['y'] - 8, 'z': 1}
    )
    osrs.move.interact_with_object_v3(
        38456,
        obj_type='ground',
        custom_exit_function=on_tomb_anchor,
    )
    osrs.move.interact_with_object_v3(
        38451,
        custom_exit_function=osrs.game.run_restored
    )
    if first_floor_only:
        osrs.move.interact_with_object_v3(
            38451,
            right_click_option='Quick-exit',
            coord_type='z',
            coord_value=0,
            greater_than=False
        )
    else:
        osrs.move.interact_with_object_v3(
            39622,
            coord_type='z',
            coord_value=2,
            greater_than=True
        )


def floor_1_scenario_2(anchor):
    osrs.dev.logger.info("Floor 1 - Scenario 2 - Anchor: %s", anchor)
    osrs.move.go_to_loc(2299 + anchor['x'], 6005 + anchor['y'], 2, skip_dax=True)
    step_1 = {
        'coord_type': 'y', 'coord_val': 6002, 'obj_id': 38411,
        'dest_x': 2299, 'dest_y': 6002, 'dest_z': 2, 'less_than': True
    }
    step_2 = {
        'coord_type': 'y', 'coord_val': 5997, 'obj_id': 38411,
        'dest_x': 2299, 'dest_y': 5997, 'dest_z': 2, 'less_than': True
    }
    step_3 = {
        'coord_type': 'y', 'coord_val': 5994, 'obj_id': 38411,
        'dest_x': 2299, 'dest_y': 5994, 'dest_z': 2, 'less_than': True
    }
    pass_flames(None, [step_1, step_2, step_3], anchor)
    osrs.move.go_to_loc(
        2303 + anchor['x'], 5986 + anchor['y'], 2, skip_dax=True, exact_tile=True, exit_on_dest=True
    )
    pass_sword(
        {'x': 2304 + anchor['x'], 'y': 5989 + anchor['y']},
        [[2301 + anchor['x'], 5978 + anchor['y'], 2]],
        {
            'x_min': 2299 + anchor['x'], 'x_max': 2303 + anchor['x'],
            'y_min': 5976 + anchor['y'], 'y_max': 5979 + anchor['y']
        },
        38439
    )
    osrs.move.go_to_loc(
        2296 + anchor['x'], 5969 + anchor['y'], 2, skip_dax=True, exact_tile=True, exit_on_dest=True
    )
    step1 = {
        'coord_type': 'x', 'coord_val': 2291, 'obj_id': 38412,
        'dest_x': 2291, 'dest_y': 5969, 'dest_z': 2
    }

    step2 = {
        'coord_type': 'x', 'coord_val': 2286, 'obj_id': 38412,
        'dest_x': 2286, 'dest_y': 5969, 'dest_z': 2
    }
    pass_flames(None, [step1, step2], anchor)
    osrs.move.interact_with_object_v3(
        38463,
        coord_type='z',
        coord_value=1,
        greater_than=False
    )
    tomb_anchor = find_second_floor_anchor(
        38458,
        {'x': 2279, 'y': 5984}
    )
    osrs.move.interact_with_object_v3(
        39524,
        coord_type='y',
        coord_value=5973 + tomb_anchor['y'],
        greater_than=False
    )
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    prev_inv = osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.HALLOWED_MARK)
    osrs.move.interact_with_object_v3(
        39544,
        custom_exit_function=inv_changed,
        custom_exit_function_arg=prev_inv
    )
    osrs.move.interact_with_object_v3(
        39524,
        coord_type='y',
        coord_value=5983 + tomb_anchor['y'],
        greater_than=True
    )
    osrs.move.interact_with_object_v3(
        38458,
        obj_type='ground',
        custom_exit_function=on_tomb_anchor
    )
    osrs.move.interact_with_object_v3(
        38451,
        custom_exit_function=osrs.game.run_restored
    )
    if first_floor_only:
        osrs.move.interact_with_object_v3(
            38451,
            right_click_option='Quick-exit',
            coord_type='z',
            coord_value=0,
            greater_than=False
        )
    else:
        osrs.move.interact_with_object_v3(
            39622,
            coord_type='z',
            coord_value=2,
            greater_than=True
        )


def floor_1_scenario_3(anchor):
    osrs.dev.logger.info("Floor 1 - Scenario 3 - Anchor: %s", anchor)
    osrs.move.go_to_loc(2268 + anchor['x'], 6014 + anchor['y'], 2, skip_dax=True)
    dodge_arrow(
        anchor, 'east', f"{2282 + anchor['x']},{6014 + anchor['y']},2",
        2266, 2283, 6016, 6018
    )
    step1 = {
        'coord_type': 'y', 'coord_val': 6009, 'obj_id': 38412,
        'dest_x': 2282, 'dest_y': 6009, 'dest_z': 2
    }

    step2 = {
        'coord_type': 'y', 'coord_val': 6004, 'obj_id': 38412,
        'dest_x': 2282, 'dest_y': 6004, 'dest_z': 2
    }
    step3 = {
        'coord_type': 'y', 'coord_val': 5994, 'obj_id': 38412,
        'dest_x': 2282, 'dest_y': 5994, 'dest_z': 2
    }
    step4 = {
        'coord_type': 'y', 'coord_val': 5991, 'obj_id': 38412,
        'dest_x': 2282, 'dest_y': 5991, 'dest_z': 2
    }
    pass_flames(None, [step1, step2, step3, step4], anchor)
    osrs.move.interact_with_object_v3(
        38462,
        coord_type='z',
        coord_value=1,
        greater_than=False
    )
    tomb_anchor = find_second_floor_anchor(
        38458,
        {'x': 2279, 'y': 5984}
    )
    osrs.move.interact_with_object_v3(
        39524,
        coord_type='y',
        coord_value=5973 + tomb_anchor['y'],
        greater_than=False
    )
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    prev_inv = osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.HALLOWED_MARK)
    osrs.move.interact_with_object_v3(
        39544,
        custom_exit_function=inv_changed,
        custom_exit_function_arg=prev_inv
    )
    osrs.move.interact_with_object_v3(
        39524,
        coord_type='y',
        coord_value=5983 + tomb_anchor['y'],
        greater_than=True
    )
    osrs.move.interact_with_object_v3(
        38458,
        obj_type='ground',
        custom_exit_function=on_tomb_anchor
    )
    osrs.move.interact_with_object_v3(
        38451,
        custom_exit_function=osrs.game.run_restored
    )
    if first_floor_only:
        osrs.move.interact_with_object_v3(
            38451,
            right_click_option='Quick-exit',
            coord_type='z',
            coord_value=0,
            greater_than=False
        )
    else:
        osrs.move.interact_with_object_v3(
            39622,
            coord_type='z',
            coord_value=2,
            greater_than=True
        )


def dodge_arrow(anchor, direction, dest, x_min, x_max, y_min, y_max):
    """

    :param anchor: {'x': 3234, 'y': -345}
    :param direction: 'north' || 'east' || 'west' || 'south'
    :param dest: '2262,3245,2'
    :return: void
    """
    tiles = osrs.util.generate_game_tiles_in_coords(
        x_min + anchor['x'], x_max + anchor['x'], y_min + anchor['y'], y_max + anchor['y'], 2
    )
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles(set(tiles))
    qh.set_tiles({dest})
    qh.set_npcs(['9672'])
    qh.set_objects_v2('game', {38444})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if f"{qh.get_player_world_location('x')},{qh.get_player_world_location('y')},{qh.get_player_world_location('z')}" == dest:
            return
        arrow = qh.get_npcs()
        if arrow:
            arrow = list(filter(
                lambda npc: is_point_in_rectangle(npc['x_coord'], npc['y_coord'], x_min + anchor['x'],
                                                  y_min + anchor['y'], x_max + anchor['x'], y_max + anchor['y'])
                            and (direction is not 'east' or npc['x_coord'] > qh.get_player_world_location('x')),
                arrow
            ))
        elif qh.get_objects_v2('game', 38444):
            arrow = list(filter(
                lambda obj: is_point_in_rectangle(obj['x_coord'], obj['y_coord'], x_min + anchor['x'],
                                                  y_min + anchor['y'], x_max + anchor['x'], y_max + anchor['y']) and
                            obj['animation'] in [8682, 8683, 8684],
                arrow
            ))
        if arrow:
            arrow = arrow[0]
        if direction == 'east':
            if arrow:
                arrow = arrow[0]
                if arrow['x_coord'] < qh.get_player_world_location('x'):
                    if qh.get_tiles(dest):
                        osrs.move.fast_click_v2(qh.get_tiles(dest))
                elif arrow['y_coord'] == qh.get_player_world_location('y'):
                    print('here112')
                    north_tile = f"{qh.get_player_world_location('x') + 1},{qh.get_player_world_location('y') + 1},{qh.get_player_world_location('z')}"
                    south_tile = f"{qh.get_player_world_location('x') + 1},{qh.get_player_world_location('y') - 1},{qh.get_player_world_location('z')}"
                    if qh.get_tiles(north_tile):
                        osrs.move.fast_click_v2(qh.get_tiles(north_tile))
                    elif qh.get_tiles(south_tile):
                        osrs.move.fast_click_v2(qh.get_tiles(south_tile))
                elif qh.get_tiles(dest):
                    osrs.move.fast_click_v2(qh.get_tiles(dest))
        elif direction == 'west':
            if arrow:
                arrow = arrow[0]
                if arrow['x_coord'] > qh.get_player_world_location('x'):
                    print('here')
                    if qh.get_tiles(dest):
                        osrs.move.fast_click_v2(qh.get_tiles(dest))
                elif arrow['y_coord'] == qh.get_player_world_location('y'):
                    print('here112')
                    north_tile = f"{qh.get_player_world_location('x') - 1},{qh.get_player_world_location('y') + 1},{qh.get_player_world_location('z')}"
                    south_tile = f"{qh.get_player_world_location('x') - 1},{qh.get_player_world_location('y') - 1},{qh.get_player_world_location('z')}"
                    if qh.get_tiles(north_tile):
                        osrs.move.fast_click_v2(qh.get_tiles(north_tile))
                    elif qh.get_tiles(south_tile):
                        osrs.move.fast_click_v2(qh.get_tiles(south_tile))
                elif qh.get_tiles(dest):
                    osrs.move.fast_click_v2(qh.get_tiles(dest))
        elif direction == 'south':
            if arrow:
                arrow = arrow[0]
                if arrow['y_coord'] > qh.get_player_world_location('y'):
                    if qh.get_tiles(dest):
                        osrs.dev.logger.debug('wuld click ss')
                        osrs.move.fast_click_v2(qh.get_tiles(dest))
                elif arrow['x_coord'] == qh.get_player_world_location('x'):
                    north_tile = f"{qh.get_player_world_location('x') + 1},{qh.get_player_world_location('y') - 1},{qh.get_player_world_location('z')}"
                    south_tile = f"{qh.get_player_world_location('x') - 1},{qh.get_player_world_location('y') - 1},{qh.get_player_world_location('z')}"
                    if qh.get_tiles(north_tile):
                        osrs.dev.logger.debug('wuld click n')
                        osrs.move.fast_click_v2(qh.get_tiles(north_tile))
                    elif qh.get_tiles(south_tile):
                        osrs.dev.logger.debug('wuld click s')
                        osrs.move.fast_click_v2(qh.get_tiles(south_tile))
                elif qh.get_tiles(dest):
                    osrs.dev.logger.debug('wuld click d')
                    osrs.move.fast_click_v2(qh.get_tiles(dest))


# 8682-4

def floor_1_scenario_4(anchor):
    osrs.dev.logger.info("Floor 1 - Scenario 4 - Anchor: %s", anchor)
    '''osrs.move.go_to_loc(2244 + anchor['x'], 5977 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    step1 = {
        'coord_type': 'y', 'coord_val': 5984, 'obj_id': 38412,
        'dest_x': 2244, 'dest_y': 5984, 'dest_z': 2
    }
    step2 = {
        'coord_type': 'y', 'coord_val': 5995, 'obj_id': 38412,
        'dest_x': 2244, 'dest_y': 5995, 'dest_z': 2
    }
    pass_flames(None, [step1, step2], anchor)
    osrs.move.go_to_loc(2240 + anchor['x'], 5997 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    pass_sword(
        {'x': 2239 + anchor['x'], 'y': 5994 + anchor['y']},
        [[2243 + anchor['x'], 6004 + anchor['y'], 2]],
        {
            'x_min': 2240 + anchor['x'], 'x_max': 2245 + anchor['x'],
            'y_min': 6004 + anchor['y'], 'y_max': 6006 + anchor['y']
        },
        38437
    )'''
    dodge_arrow(
        anchor, 'east', f"{2261 + anchor['x']},{6000 + anchor['y']},2",
        2246, 2263, 6001, 6003
    )
    osrs.move.go_to_loc(2262 + anchor['x'], 5991 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    osrs.move.interact_with_object_v3(
        38465,
        coord_type='z',
        coord_value=1,
        greater_than=False
    )
    tomb_anchor = find_second_floor_anchor(
        38456,
        {'x': 2265, 'y': 5984}
    )
    osrs.move.interact_with_object_v3(
        39527,
        coord_type='y',
        coord_value=5984 + tomb_anchor['y'] - 5,
        obj_type='ground',
        greater_than=False
    )
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    prev_inv = osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.HALLOWED_MARK)
    osrs.move.interact_with_object_v3(
        39544,
        custom_exit_function=inv_changed,
        custom_exit_function_arg=prev_inv
    )
    osrs.move.interact_with_object_v3(
        39527,
        coord_type='y',
        coord_value=5984 + tomb_anchor['y'] - 7,
        obj_type='ground',
        greater_than=True,
        obj_tile={'x': 2265 + tomb_anchor['x'] - 3, 'y': 5984 + tomb_anchor['y'] - 8, 'z': 1}
    )
    osrs.move.interact_with_object_v3(
        38456,
        obj_type='ground',
        custom_exit_function=on_tomb_anchor,
    )
    osrs.move.interact_with_object_v3(
        38451,
        custom_exit_function=osrs.game.run_restored
    )
    if first_floor_only:
        osrs.move.interact_with_object_v3(
            38451,
            right_click_option='Quick-exit',
            coord_type='z',
            coord_value=0,
            greater_than=False
        )
    else:
        osrs.move.interact_with_object_v3(
            39622,
            coord_type='z',
            coord_value=2,
            greater_than=True
        )


def determine_floor_1_layout():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {38537, 38484, 38523, 38530, 24704, 24705, 12302})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('z') == 0:
            osrs.move.interact_with_object_v3(
                38452,
                coord_type='z',
                coord_value=2,
                obj_tile={'x': 2414, 'y': 5983, 'z': 0}
            )
            osrs.clock.random_sleep(2, 2.1)
        elif qh.get_objects_v2('game', 38523) and len(qh.get_objects_v2('game', 38523)) >= 2:
            return floor_1_scenario_1({
                'x': qh.get_player_world_location('x') - 2293,
                'y': qh.get_player_world_location('y') - 5949,
            })
        elif qh.get_objects_v2('game', 38537) and len(qh.get_objects_v2('game', 38537)) >= 2:
            return floor_1_scenario_2(
                {
                    'x': qh.get_player_world_location('x') - 2309,
                    'y': qh.get_player_world_location('y') - 6011,
                }
            )
        elif qh.get_objects_v2('game', 38530) and len(qh.get_objects_v2('game', 38530)) >= 2:
            return floor_1_scenario_3(
                {
                    'x': qh.get_player_world_location('x') - 2253,
                    'y': qh.get_player_world_location('y') - 6018,
                }
            )
        elif qh.get_objects_v2('game', 24705, dist=7):
            return floor_1_scenario_4(
                {
                    'x': qh.get_player_world_location('x') - 2234,
                    'y': qh.get_player_world_location('y') - 5960,
                }
            )


def floor_2_scenario_1(anchor):
    osrs.dev.logger.info("Floor 2 - Scenario 1 - Anchor: %s", anchor)
    osrs.move.go_to_loc(2527 + anchor['x'], 5974 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    dodge_arrow(
        anchor, 'west', f"{2508 + anchor['x']},{5972 + anchor['y']},2",
        2513, 2529, 5971, 5973
    )
    osrs.move.go_to_loc(2503 + anchor['x'], 5971 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    pass_floor_objs(2502 + anchor['x'], 2504 + anchor['x'], 5967 + anchor['y'], 5967 + anchor['y'], 2)
    pass_sword(
        {'x': 2502 + anchor['x'], 'y': 5962 + anchor['y']},
        [[2493 + anchor['x'], 5957 + anchor['y'], 2]],
        {
            'x_min': 2490 + anchor['x'], 'x_max': 2510 + anchor['x'],
            'y_min': 5956 + anchor['y'], 'y_max': 5958 + anchor['y']
        },
        38436,
        on_npc_position=True
    )
    osrs.move.go_to_loc(2517 + anchor['x'], 5960 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    # from here i will sacrifice the ashes to loot chest
    prev_inv = get_prev_inv(osrs.item_ids.VAMPYRE_DUST)
    osrs.move.interact_with_object_v3(
        39526,
        custom_exit_function=inv_changed,
        custom_exit_function_arg=prev_inv
    )
    prev_inv = get_prev_inv(osrs.item_ids.VAMPYRE_DUST)
    osrs.move.interact_with_object_v3(
        39525,
        custom_exit_function=inv_changed_v2,
        custom_exit_function_arg=[prev_inv, osrs.item_ids.VAMPYRE_DUST],
    )
    osrs.move.interact_with_object_v3(
        39534,
        coord_type='x',
        coord_value=2520 + anchor['x'],
        right_click_option='Pass-through',
        greater_than=True,
        timeout=3
    )
    prev_inv = get_prev_inv(osrs.item_ids.HALLOWED_MARK)
    osrs.move.interact_with_object_v3(
        39544,
        custom_exit_function=inv_changed_v2,
        custom_exit_function_arg=[prev_inv, osrs.item_ids.HALLOWED_MARK]
    )
    osrs.move.interact_with_object_v3(
        39534,
        coord_type='x',
        coord_value=2520 + anchor['x'],
        right_click_option='Pass-through',
        greater_than=False,
        timeout=3
    )
    osrs.move.interact_with_object_v3(
        38468,
        coord_type='z',
        coord_value=1,
        greater_than=False
    )
    anchor = find_floor_anchor_with_player_loc({'x': 2511, 'y': 5969}, 1)
    dodge_arrow(
        anchor, 'east', f"{2528 + anchor['x']},{5975 + anchor['y']},1",
        2504, 2530, 5971, 5973
    )
    osrs.move.interact_with_object_v3(
        38455,
        obj_type='ground',
        coord_type='y',
        coord_value=5977 + anchor['y'],
        greater_than=True
    )
    if second_floor_only:
        osrs.move.interact_with_object_v3(
            38451,
            right_click_option='Quick-exit',
            coord_type='z',
            coord_value=0,
            greater_than=False
        )
    else:
        osrs.move.interact_with_object_v3(
            39623,
            coord_type='z',
            coord_value=2,
            greater_than=True
        )


def pass_floor_objs(dest_x_min, dest_x_max, dest_y_min, dest_y_max, dest_z=2):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if is_point_in_rectangle(
                qh.get_player_world_location('x'), qh.get_player_world_location('y'),
                dest_x_min, dest_y_min, dest_x_max, dest_y_max
        ):
            osrs.dev.logger.info("Successfully passed floor puzzle")
            return
        osrs.dev.logger.info("Navigating over floor puzzle")
        osrs.move.go_to_loc(
            math.floor((dest_x_max + dest_x_min) / 2),
            math.floor((dest_y_max + dest_y_min) / 2),
            dest_z,
            skip_dax=True, exit_on_dest=True
        )


def floor_2_scenario_4(anchor):
    osrs.dev.logger.info("Floor 2 - Scenario 4 - Anchor: %s", anchor)
    osrs.move.go_to_loc(2536 + anchor['x'], 5984 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    # TODO not sure if these floor x coords are right
    step1 = {
        'coord_type': 'x', 'coord_val': 2543, 'obj_id': 38409,
        'dest_x': 2543, 'dest_y': 5984, 'dest_z': 2
    }
    step2 = {
        'coord_type': 'x', 'coord_val': 2551, 'obj_id': 38409,
        'dest_x': 2551, 'dest_y': 5984, 'dest_z': 2
    }
    pass_flames(None, [step1, step2], anchor)
    osrs.move.go_to_loc(2553 + anchor['x'], 5975 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    qh = osrs.queryHelper.QueryHelper()
    qh.set_yaw(1024)
    qh.query_backend()
    dodge_arrow(
        anchor, 'south', f"{2553 + anchor['x']},{5956 + anchor['y']},2",
        2554, 2556, 5955, 5975
    )
    qh.set_yaw(0)
    qh.query_backend()
    pass_floor_objs(
        2538 + anchor['x'], 2541 + anchor['x'], 5955 + anchor['y'], 5961 + anchor['y'], 2
    )
    prev_inv = get_prev_inv(osrs.item_ids.VAMPYRE_DUST)
    osrs.move.interact_with_object_v3(
        39525,
        custom_exit_function=inv_changed_v2,
        custom_exit_function_arg=[prev_inv, osrs.item_ids.VAMPYRE_DUST],
    )
    osrs.move.interact_with_object_v3(
        39534,
        coord_type='x',
        coord_value=2528 + anchor['x'],
        right_click_option='Pass-through',
        greater_than=False,
        timeout=3
    )
    prev_inv = get_prev_inv(osrs.item_ids.HALLOWED_MARK)
    osrs.move.interact_with_object_v3(
        39544,
        custom_exit_function=inv_changed_v2,
        custom_exit_function_arg=[prev_inv, osrs.item_ids.HALLOWED_MARK]
    )
    osrs.move.interact_with_object_v3(
        39534,
        coord_type='x',
        coord_value=2528 + anchor['x'],
        right_click_option='Pass-through',
        greater_than=True,
        timeout=3
    )
    osrs.move.interact_with_object_v3(
        38467,
        coord_type='z',
        coord_value=1,
        greater_than=False
    )
    anchor = find_floor_anchor_with_player_loc({'x': 2555, 'y': 5958}, 1)
    osrs.move.go_to_loc(2555 + anchor['x'], 5970 + anchor['y'], 1, skip_dax=True, exit_on_dest=True)
    step1 = {
        'coord_type': 'y', 'coord_val': 5977, 'obj_id': 38412,
        'dest_x': 2555, 'dest_y': 5977, 'dest_z': 1
    }
    step2 = {
        'coord_type': 'y', 'coord_val': 5984, 'obj_id': 38411,
        'dest_x': 2555, 'dest_y': 5984, 'dest_z': 1
    }
    pass_flames(None, [step1, step2], anchor)
    osrs.move.go_to_loc(2546 + anchor['x'], 5984 + anchor['y'], 1, skip_dax=True, exit_on_dest=True)
    step1 = {
        'coord_type': 'x', 'coord_val': 2538, 'obj_id': 38412,
        'dest_x': 2538, 'dest_y': 5984, 'dest_z': 1
    }
    pass_flames(None, [step1], anchor)
    osrs.move.interact_with_object_v3(
        38458,
        obj_type='ground',
        coord_type='x',
        coord_value=2535 + anchor['x'],
        greater_than=False
    )
    osrs.move.interact_with_object_v3(
        38451,
        custom_exit_function=osrs.game.run_restored
    )
    if second_floor_only:
        osrs.move.interact_with_object_v3(
            38451,
            right_click_option='Quick-exit',
            coord_type='z',
            coord_value=0,
            greater_than=False
        )
    else:
        osrs.move.interact_with_object_v3(
            39623,
            coord_type='z',
            coord_value=2,
            greater_than=True
        )


def floor_2_scenario_2(anchor):
    osrs.dev.logger.info("Floor 2 - Scenario 2 - Anchor: %s", anchor)
    osrs.move.go_to_loc(2513 + anchor['x'], 5987 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    pass_sword(
        {'x': 2512 + anchor['x'], 'y': 5985 + anchor['y']},
        [[2506 + anchor['x'], 5996 + anchor['y'], 2]],
        {
            'x_min': 2504 + anchor['x'], 'x_max': 2508 + anchor['x'],
            'y_min': 5995 + anchor['y'], 'y_max': 6004 + anchor['y']
        },
        38436
    )
    # next chest is looted here
    osrs.move.go_to_loc(2511 + anchor['x'], 6004 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    prev_inv = get_prev_inv(osrs.item_ids.HALLOWED_MARK)
    osrs.move.interact_with_object_v3(
        39524,
        coord_type='x',
        coord_value=2522 + anchor['x'],
        greater_than=True
    )
    osrs.clock.sleep_one_tick()
    osrs.clock.sleep_one_tick()
    osrs.clock.sleep_one_tick()
    osrs.clock.sleep_one_tick()
    osrs.move.interact_with_object_v3(
        39544,
        custom_exit_function=inv_changed,
        custom_exit_function_arg=prev_inv
    )
    osrs.move.interact_with_object_v3(
        39524,
        coord_type='x',
        coord_value=2512 + anchor['x'],
        greater_than=False
    )
    osrs.move.go_to_loc(2493 + anchor['x'], 6009 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    pass_floor_objs(
        2492 + anchor['x'], 2494 + anchor['x'], 5994 + anchor['y'], 5997 + anchor['y']
    )
    osrs.move.go_to_loc(2488 + anchor['x'], 5988 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    step1 = {
        'coord_type': 'y', 'coord_val': 5984, 'obj_id': 38409,
        'dest_x': 2488, 'dest_y': 5984, 'dest_z': 2
    }
    step2 = {
        'coord_type': 'y', 'coord_val': 5979, 'obj_id': 38409,
        'dest_x': 2488, 'dest_y': 5979, 'dest_z': 2
    }
    pass_flames(None, [step1, step2], anchor)
    osrs.move.interact_with_object_v3(
        38469,
        coord_type='z',
        coord_value=1,
        greater_than=False,
        right_click_option='Jump',
        timeout=5
    )
    anchor = find_floor_anchor_with_player_loc({'x': 2493, 'y': 5977}, 1)
    osrs.move.go_to_loc(2497 + anchor['x'], 5982 + anchor['y'], 1, skip_dax=True, exit_on_dest=True)
    pass_sword(
        {'x': 2494 + anchor['x'], 'y': 5983 + anchor['y']},
        [[2515 + anchor['x'], 5984 + anchor['y'], 1]],
        {
            'x_min': 2513 + anchor['x'], 'x_max': 2520 + anchor['x'],
            'y_min': 5979 + anchor['y'], 'y_max': 5989 + anchor['y']
        },
        38436
    )
    osrs.move.interact_with_object_v3(
        38456,
        obj_type='ground',
        coord_type='x',
        coord_value=2523 + anchor['x']
    )
    osrs.move.interact_with_object_v3(
        38451,
        custom_exit_function=osrs.game.run_restored
    )
    if second_floor_only:
        osrs.move.interact_with_object_v3(
            38451,
            right_click_option='Quick-exit',
            coord_type='z',
            coord_value=0,
            greater_than=False
        )
    else:
        osrs.move.interact_with_object_v3(
            39623,
            coord_type='z',
            coord_value=2,
            greater_than=True
        )


def floor_2_scenario_3(anchor):
    osrs.dev.logger.info("Floor 2 - Scenario 3 - Anchor: %s", anchor)
    osrs.move.go_to_loc(2518 + anchor['x'], 5998 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    osrs.move.interact_with_object_v3(
        38470,
        coord_type='y',
        coord_value=6009 + anchor['y'],
        obj_type='ground'
    )
    dodge_arrow(
        anchor, 'east', f"{2529 + anchor['x']},{6016 + anchor['y']},2",
        2516, 2527, 6012, 6014
    )
    osrs.move.go_to_loc(2536 + anchor['x'], 6015 + anchor['y'], 2, skip_dax=True, exit_on_dest=True)
    pass_sword(
        {'x': 2533 + anchor['x'], 'y': 6014 + anchor['y']},
        [[2546 + anchor['x'], 6008 + anchor['y'], 1]],
        {
            'x_min': 2546 + anchor['x'], 'x_max': 2548 + anchor['x'],
            'y_min': 6005 + anchor['y'], 'y_max': 6010 + anchor['y']
        },
        38436
    )
    # next chest is looted here
    prev_inv = get_prev_inv(osrs.item_ids.HALLOWED_MARK)
    osrs.move.interact_with_object_v3(
        39524,
        coord_type='x',
        coord_value=2534 + anchor['x'],
        greater_than=False
    )
    osrs.move.interact_with_object_v3(
        39544,
        custom_exit_function=inv_changed,
        custom_exit_function_arg=prev_inv
    )
    osrs.move.interact_with_object_v3(
        39524,
        coord_type='x',
        coord_value=2544 + anchor['x'],
        greater_than=True
    )
    osrs.move.interact_with_object_v3(
        38466,
        coord_type='z',
        coord_value=1,
        greater_than=False
    )
    anchor = find_floor_anchor_with_player_loc({'x': 2548, 'y': 6008}, 1)
    osrs.move.go_to_loc(2545 + anchor['x'], 6013 + anchor['y'], 1, skip_dax=True, exit_on_dest=True)
    pass_floor_objs(
        2527 + anchor['x'], 2531 + anchor['x'], 6012 + anchor['y'], 6014 + anchor['y']
    )
    osrs.move.go_to_loc(2528 + anchor['x'], 6010 + anchor['y'], 1, skip_dax=True, exit_on_dest=True)
    step1 = {
        'coord_type': 'y', 'coord_val': 6005, 'obj_id': 38409,
        'dest_x': 2528, 'dest_y': 6005, 'dest_z': 1
    }
    step2 = {
        'coord_type': 'y', 'coord_val': 5999, 'obj_id': 38410,
        'dest_x': 2528, 'dest_y': 5999, 'dest_z': 1
    }
    pass_flames(None, [step1, step2], anchor)
    osrs.move.interact_with_object_v3(
        38457,
        coord_type='y',
        coord_value=5991 + anchor['y'],
        obj_type='ground',
        greater_than=False
    )
    osrs.move.interact_with_object_v3(
        38451,
        custom_exit_function=osrs.game.run_restored
    )
    if second_floor_only:
        osrs.move.interact_with_object_v3(
            38451,
            right_click_option='Quick-exit',
            coord_type='z',
            coord_value=0,
            greater_than=False
        )
    else:
        osrs.move.interact_with_object_v3(
            39623,
            coord_type='z',
            coord_value=2,
            greater_than=True
        )


def determine_floor_2_layout():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {38537, 38484, 38523, 38530, 24704, 12302})
    qh.set_objects_v2('decorative', {38909})
    qh.set_player_world_location()
    qh.set_players()
    '''
    0 is south - opt 1
    512 is west - opt 2
    1024 is north - opt 3
    1536 is east - opt 4
    '''
    while True:
        qh.query_backend()
        local_player = qh.get_players(get_own_player=True)
        if local_player and local_player['orientation'] == 1536:
            return floor_2_scenario_4({
                'x': qh.get_player_world_location('x') - 2532,
                'y': qh.get_player_world_location('y') - 5984,
            })
        elif local_player and local_player['orientation'] == 512:
            return floor_2_scenario_2({
                'x': qh.get_player_world_location('x') - 2524,
                'y': qh.get_player_world_location('y') - 5984,
            })
        elif local_player and local_player['orientation'] == 1024:
            return floor_2_scenario_3({
                'x': qh.get_player_world_location('x') - 2528,
                'y': qh.get_player_world_location('y') - 5988,
            })
        elif local_player and local_player['orientation'] == 0:
            return floor_2_scenario_1({
                'x': qh.get_player_world_location('x') - 2528,
                'y': qh.get_player_world_location('y') - 5980,
            })


# enter 39622 and z == 2
equipment = [
    {'id': osrs.item_ids.ADAMANT_CROSSBOW, 'consume': 'Wield'},
    {'id': osrs.item_ids.MITH_GRAPPLE_9419, 'consume': 'Wield'},
    {'id': osrs.item_ids.GRACEFUL_TOP, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_CAPE, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_HOOD, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_LEGS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_GLOVES, 'consume': 'Wear'},
    {'id': osrs.item_ids.HOLY_SYMBOL, 'consume': 'Wear'},
]
supplies = [
    {'id': osrs.item_ids.HAMMER},
    {'id': osrs.item_ids.SAW},
    {'id': [
        osrs.item_ids.STEEL_NAILS
    ],
        'quantity': 'All'
    },
    {'id': osrs.item_ids.VAMPYRE_DUST},
    {'id': osrs.item_ids.VAMPYRE_DUST},
    {'id': osrs.item_ids.VAMPYRE_DUST},
    {'id': osrs.item_ids.VAMPYRE_DUST},
    {'id': osrs.item_ids.PLANK},
    {'id': osrs.item_ids.PLANK},
    {'id': osrs.item_ids.PLANK},
    {'id': osrs.item_ids.PLANK},
]


def main():
    if not osrs.player.is_equipped([item['id'] for item in equipment]):
        osrs.bank.banking_handler({
            'dump_equipment': True,
            'dump_inv': True,
            'search': [{'query': 'hallowed', 'items': equipment}]
        })
    while True:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_inventory()
        if len(qh.get_inventory()) >= 24 \
                or osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.PLANK) < 4 \
                or osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.VAMPYRE_DUST) < 4:
            osrs.bank.banking_handler({
                'dump_inv': True,
                'search': [{'query': 'hallowed', 'items': supplies}]
            })
        determine_floor_1_layout()
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        osrs.clock.sleep_one_tick()
        determine_floor_2_layout()


#main()
floor_1_scenario_4({'x': 7696, 'y': -1072})
