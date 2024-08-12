import datetime

import osrs

logger = osrs.dev.instantiate_logger()
ore_veins = {
    '26661',
    '26662',
    '26663',
    '26664',
}

ore_locs = {
    '3759,5674,0',
    '3760,5674,0',
    '3761,5674,0',
    '3762,5673,0',
    '3762,5672,0',
    '3762,5671,0',
    '3762,5670,0',
}

loot = [
    osrs.item_ids.ItemIDs.GOLDEN_NUGGET.value,
    osrs.item_ids.ItemIDs.RUNITE_ORE.value,
    osrs.item_ids.ItemIDs.ADAMANTITE_ORE.value,
    osrs.item_ids.ItemIDs.MITHRIL_ORE.value,
    osrs.item_ids.ItemIDs.GOLD_ORE.value,
    osrs.item_ids.ItemIDs.COAL.value,
]

rockfall_id = '26679'  # game object id


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
        if qh.get_player_world_location('x') >= 3758 and qh.get_player_world_location('y') >= 5675:
            if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, rockfall_id):
                osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, rockfall_id)[0])
            elif (qh.get_tiles('3761,5670,0')
                  and (datetime.datetime.now() - last_return_tile_click).total_seconds() > 2.3):
                osrs.move.fast_click(qh.get_tiles('3761,5670,0'))
                last_return_tile_click = datetime.datetime.now()
        elif qh.get_varbit() and qh.get_varbit() + osrs.inv.get_item_quantity_in_inv(qh.get_inventory() or [], osrs.item_ids.ItemIDs.PAYDIRT.value) >= 189:
            logger.info('at 189 paydirt.')
            return True
        elif qh.get_inventory() and len(qh.get_inventory()) == 28:
            logger.info('inv is full, done mining.')
            return False
        elif not qh.get_is_mining() and (datetime.datetime.now() - last_mining).total_seconds() > 1.5:
            logger.info('have not been mining for over 1.5 seconds.')
            if qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value) and (
                    datetime.datetime.now() - last_ore_click).total_seconds() > 3:
                all_veins = osrs.util.combine_objects(qh.get_objects(osrs.queryHelper.ObjectTypes.WALL.value))
                c = osrs.util.find_closest_target(all_veins)
                if c:
                    logger.info('clicking another ore vein.')
                    res = osrs.move.right_click_v6(
                        c,
                        'Mine',
                        qh.get_canvas()
                    )
                    if res:
                        last_ore_click = datetime.datetime.now()
        elif qh.get_is_mining():
            logger.info('currently mining.')
            last_mining = datetime.datetime.now()


def deposit_ore():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_varbit('5558')
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.PAYDIRT.value) or qh.get_varbit() >= 189:
        return True


def should_collect(current_paydirt):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_varbit('5558')
    qh.query_backend()
    if qh.get_varbit() and qh.get_varbit() + current_paydirt >= 189:
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
    logger.info('beginning ore collection.')
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
            logger.info('Sack emptied, exiting.')
            return
        elif not qh.get_inventory(loot) and qh.get_objects(osrs.queryHelper.ObjectTypes.GROUND.value, ore_sack):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GROUND.value, ore_sack)[0])
            logger.info('clicking ore sack.')
        elif qh.get_inventory(loot):
            if qh.get_widgets(deposit_all_button):
                logger.info('at deposit box, depositing all ore.')
                osrs.move.fast_click(qh.get_widgets(deposit_all_button))
                osrs.clock.sleep_one_tick()
                osrs.keeb.press_key('esc')
            elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, deposit_box) and \
                    (datetime.datetime.now() - last_deposit_box_click).total_seconds() > 4.2:
                logger.info('depositing ore and nuggets in bank.')
                res = osrs.move.right_click_v6(
                    qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, deposit_box)[0],
                    'Deposit',
                    qh.get_canvas()
                )
                if res:
                    last_deposit_box_click = datetime.datetime.now()

osrs.move.go_to_loc(3761,5672)
while True:
    osrs.game.break_manager_v4({
        'intensity': 'high',
        'login': False,
        'logout': False
    })
    should_collect = mine_ore()
    logger.info('depositing ore')
    osrs.move.interact_with_object(
        26674, 'y', 5673, False, custom_exit_function=deposit_ore, timeout=10,
        obj_tile={'x': 3755, 'y': 5677, 'z': 0}, right_click_option='Deposit'
    )
    osrs.clock.random_sleep(1, 1.01)
    if should_collect:
        logger.info('heading to lower level.')
        osrs.move.interact_with_object(
            19045, 'y', 5673, False,
            custom_exit_function=descended_ladder, right_click_option='Climb', timeout=3
        )
        logger.info('need to collect ore, going to ore sack.')
        osrs.move.go_to_loc(3748, 5659)
        collect_ore()
        osrs.move.interact_with_object(
            19044, 'y', 5674, True, intermediate_tile='3755,5668,0',
            custom_exit_function=ascended_ladder, right_click_option='Climb', timeout=3
        )
    osrs.move.go_to_loc(3761, 5672)
