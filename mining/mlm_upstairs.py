import datetime
import random

import osrs

ore_veins = {
    '26661',
    '26662',
    '26663',
    '26664',
}

ore_locs = {
    '3751,5680,0',
    '3751,5681,0',
    '3753,5680,0',
    '3749,5682,0',
    '3748,5682,0',
    '3754,5682,0', ##
    '3754,5683,0', ##
    '3752,5684,0',
}

loot = [
    osrs.item_ids.GOLDEN_NUGGET,
    osrs.item_ids.RUNITE_ORE,
    osrs.item_ids.ADAMANTITE_ORE,
    osrs.item_ids.MITHRIL_ORE,
    osrs.item_ids.GOLD_ORE,
    osrs.item_ids.COAL,
]

equipment = [
    {'id': osrs.item_ids.GRACEFUL_TOP, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_CAPE, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_HOOD, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_LEGS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.GRACEFUL_GLOVES, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAGON_PICKAXE, 'consume': 'Wield'},
    {'id': [
            osrs.item_ids.SKILLS_NECKLACE1,
            osrs.item_ids.SKILLS_NECKLACE2,
            osrs.item_ids.SKILLS_NECKLACE3,
            osrs.item_ids.SKILLS_NECKLACE4,
            osrs.item_ids.SKILLS_NECKLACE5,
            osrs.item_ids.SKILLS_NECKLACE6,
        ], 'consume': 'Wear'},
]


rockfall_id = '26679'  # game object id


def start_function():
    osrs.game.slow_lumb_tele()
    osrs.move.go_to_loc(3208, 3211)
    osrs.move.interact_with_object_v3(
        14880, obj_type='ground', coord_type='y', coord_value=9000,
        greater_than=True, right_click_option='Climb-down', timeout=8
    )
    osrs.bank.banking_handler({
        'dump_equipment': True,
        'dump_inv': True,
        'search': [{'query': 'mlm', 'items': equipment}]
    })
    osrs.game.skills_tele('Mining')
    osrs.move.interact_with_object_v3(
        26654, obj_type='game', coord_type='y', coord_value=9000,
        greater_than=False, right_click_option='Enter', timeout=8
    )
    osrs.move.interact_with_object_v3(
        26680, obj_type='game', coord_type='x', coord_value=3733,
        greater_than=True, intermediate_tile='3733,5681,0', obj_tile={'x': 3731, 'y': 5683, 'z': 0}
    )
    osrs.move.interact_with_object_v3(
        26679, obj_type='game', coord_type='x', coord_value=3736,
        greater_than=True, intermediate_tile='3736,5678,0', obj_tile={'x': 3733, 'y': 5680, 'z': 0}
    )
    osrs.move.go_to_loc(3750, 5670)
    osrs.move.interact_with_object(
        19044, 'y', 5674, True, intermediate_tile='3755,5668,0',
        custom_exit_function=ascended_ladder, right_click_option='Climb', timeout=3
    )


def mine_ore():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_is_mining()
    qh.set_varbit('5558')
    qh.set_player_world_location()
    qh.set_canvas()
    qh.set_objects(
        ore_locs,
        ore_veins,
        osrs.queryHelper.ObjectTypes.WALL.value
    )
    qh.set_objects(
        {'3757,5677,0'},
        {rockfall_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_tiles({'3761,5672,0'})
    last_mining = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_ore_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_return_tile_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_varbit() and qh.get_varbit() + osrs.inv.get_item_quantity_in_inv(qh.get_inventory() or [], osrs.item_ids.PAYDIRT) >= 108:
            osrs.dev.logger.info('at 189 paydirt.')
            return True
        elif qh.get_inventory() and len(qh.get_inventory()) == 28:
            osrs.dev.logger.info('inv is full, done mining.')
            return False
        elif not qh.get_is_mining() and (datetime.datetime.now() - last_mining).total_seconds() > 1.5:
            osrs.dev.logger.info('have not been mining for over 1.5 seconds.')
            if qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value) and (
                    datetime.datetime.now() - last_ore_click).total_seconds() > 3.0:
                all_veins = osrs.util.combine_objects(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value))
                c = osrs.util.find_closest_target(all_veins)
                if c:
                    osrs.dev.logger.info('clicking another ore vein.')
                    res = osrs.move.right_click_v6(
                        c,
                        'Mine',
                        qh.get_canvas()
                    )
                    if res:
                        last_ore_click = datetime.datetime.now()
        elif qh.get_is_mining():
            osrs.dev.logger.info('currently mining.')
            last_mining = datetime.datetime.now()


def deposit_ore():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_varbit('5558')
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.PAYDIRT) or qh.get_varbit() >= 108:
        return True


def should_collect(current_paydirt):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_varbit('5558')
    qh.query_backend()
    if qh.get_varbit() and qh.get_varbit() + current_paydirt >= 108:
        return True


def descended_ladder():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_player_world_location('x') <= 3756 and qh.get_player_world_location('y') <= 5673:
        return True


def ascended_ladder():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if qh.get_player_world_location('x') >= 3755 and qh.get_player_world_location('y') >= 5674:
        return True


def collect_ore():
    osrs.dev.logger.info('beginning ore collection.')
    deposit_all_button = '192,4'
    ore_sack = '26688'
    deposit_box = '25937'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_varbit('5558')
    qh.set_inventory()
    qh.set_canvas()
    qh.set_widgets({deposit_all_button})
    qh.set_objects(
        {'3748,5659,0'},
        {ore_sack},
        osrs.queryHelper.ObjectTypes.GROUND.value
    )
    qh.set_objects(
        {'3759,5664,0'},
        {deposit_box},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    last_deposit_box_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if (not qh.get_varbit() or qh.get_varbit() == 0) and not qh.get_inventory(loot):
            osrs.dev.logger.info('Sack emptied, exiting.')
            return
        elif not qh.get_inventory(loot) and qh.get_objects(osrs.queryHelper.ObjectTypes.GROUND.value, ore_sack):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GROUND.value, ore_sack)[0])
            osrs.dev.logger.info('clicking ore sack.')
        elif qh.get_inventory(loot):
            if qh.get_widgets(deposit_all_button):
                osrs.dev.logger.info('at deposit box, depositing all ore.')
                osrs.move.fast_click(qh.get_widgets(deposit_all_button))
                osrs.clock.sleep_one_tick()
                osrs.keeb.press_key('esc')
            elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, deposit_box) and \
                    (datetime.datetime.now() - last_deposit_box_click).total_seconds() > 7:
                osrs.dev.logger.info('depositing ore and nuggets in bank.')
                res = osrs.move.right_click_v6(
                    qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, deposit_box)[0],
                    'Deposit',
                    qh.get_canvas()
                )
                if res:
                    last_deposit_box_click = datetime.datetime.now()


def main(endless_loop=True):
    # number of times to run this script
    iter_count = 9999 if endless_loop else random.randint(3, 5)
    start_function()
    while True:
        break_info = osrs.game.break_manager_v4({
            'intensity': 'high',
            'login': False,
            'logout': False
        })
        if iter_count == 0:
            return
        elif 'took_break' in break_info and break_info['took_break']:
            iter_count -= 1
        paydirt_count = mine_ore()
        osrs.dev.logger.info('heading to lower level.')
        osrs.move.interact_with_object(
            19045, 'y', 5673, False,
            custom_exit_function=descended_ladder, right_click_option='Climb', timeout=3
        )
        osrs.dev.logger.info('depositing ore')
        osrs.move.interact_with_object(
            26674, 'y', 5673, False, custom_exit_function=deposit_ore, timeout=9,
            right_click_option='Deposit'
        )
        if should_collect(paydirt_count):
            osrs.dev.logger.info('need to collect ore, going to ore sack.')
            osrs.move.go_to_loc(3748, 5659)
            collect_ore()
        osrs.move.interact_with_object(
            19044, 'y', 5674, True, intermediate_tile='3755,5668,0',
            custom_exit_function=ascended_ladder, right_click_option='Climb', timeout=6
        )


