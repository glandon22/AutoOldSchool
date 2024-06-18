import datetime
import osrs

enriched_bone_id = '21553'
logger = osrs.dev.instantiate_logger()

run_energy_widget_id = '160,28'
bank_dump_widget_id = '12,42'
fancy_restore_pool_id = '29241'
mounted_digsite_pendant_id = '33417'
mush_tree_tile = '3765,3880,1'
mush_meadow_button_id = '608,15'
mush_tree_id = '30920'

fossil_id = '21568'

target_text_color = 65280
unid_fossil_widget_id = '613,16'
add_calcium_widget = '613,23'
add_phosphate_widget = '613,28'
fossil_count_widget = '613,35'
calcium_amount_widget = '613,26'
phosphate_amount_widget = '613,31'
chemical_process_notification_widget = '229,1'


def mushtree_to_meadow():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        {mush_tree_tile},
        {mush_tree_id}
    )
    qh.set_widgets({mush_meadow_button_id, bank_dump_widget_id})
    qh.set_player_world_location()
    logger.info('searching for mushtree to travel to meadow.')
    last_mushtree_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_swamp_press = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(mush_meadow_button_id) and (datetime.datetime.now() - last_swamp_press).total_seconds() > 5:
            logger.info('mushtree teleport menu open, selecting meadow.')
            osrs.keeb.write('4')
            last_swamp_press = datetime.datetime.now()
        elif qh.get_player_world_location() and qh.get_player_world_location()['x'] < 3700:
            logger.info('in mushroom meadow.')
            return
        elif qh.get_game_objects(mush_tree_id) and (datetime.datetime.now() - last_mushtree_click).total_seconds() > 8:
            osrs.move.click(qh.get_game_objects(mush_tree_id)[0])
            last_mushtree_click = datetime.datetime.now()
            logger.info('Clicked mushtree.')


def click_mounted_digsite_pendant():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        {mush_tree_tile},
        {mush_tree_id}
    )
    qh.set_widgets({mush_meadow_button_id, bank_dump_widget_id, run_energy_widget_id})
    qh.set_player_world_location()
    qh.set_script_stats({'Status': 'Returning to Fossil Island.'})
    logger.info('Looking for digsite pendant')
    tile_map = None
    last_pendant_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_pool_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') > 4000 and not tile_map:
            logger.info('in house, generating tile map.')
            tile_map = osrs.util.generate_game_tiles_in_coords(
                qh.get_player_world_location('x') - 15,
                qh.get_player_world_location('x') + 15,
                qh.get_player_world_location('y') - 15,
                qh.get_player_world_location('y') + 15,
                1
            )
            qh.set_objects(set(tile_map), set(), osrs.queryHelper.ObjectTypes.DECORATIVE.value)
            qh.set_objects(set(tile_map), {fancy_restore_pool_id}, osrs.queryHelper.ObjectTypes.GAME.value)
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, fancy_restore_pool_id) and \
                (datetime.datetime.now() - last_pool_click).total_seconds() > 12 \
                and (qh.get_widgets(run_energy_widget_id) and int(qh.get_widgets(run_energy_widget_id)['text']) < 95):

            logger.info('Click on ornate rejuvenation pool.')
            osrs.move.click(
                qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value)[fancy_restore_pool_id][0]
            )
            last_pool_click = datetime.datetime.now()
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.DECORATIVE.value, mounted_digsite_pendant_id) and \
                (datetime.datetime.now() - last_pendant_click).total_seconds() > 7 \
                and (qh.get_widgets(run_energy_widget_id) and int(qh.get_widgets(run_energy_widget_id)['text']) == 100):
            logger.info('clicking on digsite pendant')
            osrs.move.click(
                qh.get_objects(osrs.queryHelper.ObjectTypes.DECORATIVE.value)[mounted_digsite_pendant_id][0]
            )
            last_pendant_click = datetime.datetime.now()
        elif 3840 < qh.get_player_world_location('y') < 3900:
            logger.info('successfully teleported to fossil island.')
            return


def run_to_hopper():
    hopper_id = '30973'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'3689,3881,0'},
        {hopper_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_target_obj()
    qh.set_widgets({'613,0'})
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        # interface is open
        if qh.get_widgets('613,0') and qh.get_widgets('613,0')['x'] != -1:
            print(qh.get_widgets('613,0'))
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, hopper_id) \
                and (
                    qh.get_target_obj() != int(hopper_id) or (datetime.datetime.now() - last_click).total_seconds() > 12
        ):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, hopper_id)[0])
            last_click = datetime.datetime.now()


def add_fossils():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({
        unid_fossil_widget_id, add_calcium_widget, add_phosphate_widget,
        fossil_count_widget, calcium_amount_widget, phosphate_amount_widget
    })
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory() and len(qh.get_inventory()) > 4:
            logger.info('loading fossils')
            if qh.get_widgets(unid_fossil_widget_id):
                osrs.move.fast_click(qh.get_widgets(unid_fossil_widget_id))
                logger.info('adding more fossils')
        elif qh.get_widgets(calcium_amount_widget) and qh.get_widgets(calcium_amount_widget)['textColor'] != target_text_color:
            if qh.get_widgets(add_calcium_widget):
                osrs.move.click(qh.get_widgets(add_calcium_widget))
        elif qh.get_widgets(phosphate_amount_widget) and qh.get_widgets(phosphate_amount_widget)['textColor'] != target_text_color:
            if qh.get_widgets(add_phosphate_widget):
                osrs.move.click(qh.get_widgets(add_phosphate_widget))
        elif qh.get_inventory() and len(qh.get_inventory()) == 4 \
            and qh.get_widgets(calcium_amount_widget)['textColor'] == target_text_color \
                and qh.get_widgets(phosphate_amount_widget)['textColor'] == target_text_color:
            logger.info('fossils and chemicals loaded')
            osrs.keeb.press_key('esc')
            return


def enrich_bones():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({chemical_process_notification_widget})
    qh.set_npcs_by_name(['bobbing fossil'])
    while True:
        qh.query_backend()
        if qh.get_widgets(chemical_process_notification_widget) and 'chemical process in the pool has finished' in qh.get_widgets(chemical_process_notification_widget)['text']:
            return
        elif qh.get_npcs_by_name():
            closest = osrs.util.find_closest_target(qh.get_npcs_by_name())
            if closest:
                osrs.move.fast_click(closest)


def mushtree_to_house_on_hill():
    mush_tree_id_meadow = '30924'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        {'3675,3871,0'},
        {mush_tree_id_meadow}
    )
    qh.set_widgets({mush_meadow_button_id, bank_dump_widget_id})
    qh.set_player_world_location()
    logger.info('searching for mushtree to travel to house.')
    qh.query_backend()
    osrs.move.follow_path(qh.get_player_world_location(), {'x': 3678, 'y': 3871, 'z': 0})
    last_mushtree_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_swamp_press = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_widgets(mush_meadow_button_id) and (datetime.datetime.now() - last_swamp_press).total_seconds() > 5:
            logger.info('mushtree teleport menu open, selecting meadow.')
            osrs.keeb.write('1')
            last_swamp_press = datetime.datetime.now()
        elif qh.get_player_world_location() and 3760 <= qh.get_player_world_location()['x'] < 3768 \
                and 3876 <= qh.get_player_world_location()['y'] < 3883:
            logger.info('in house on hill.')
            return
        elif qh.get_game_objects(mush_tree_id_meadow) and (datetime.datetime.now() - last_mushtree_click).total_seconds() > 8:
            osrs.move.click(qh.get_game_objects(mush_tree_id_meadow)[0])
            last_mushtree_click = datetime.datetime.now()
            logger.info('Clicked mushtree.')


def add_bones_to_strange_machine():
    machine_id = '30945'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_objects(
        {'3770,3869,1'},
        {machine_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    last_machine_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if qh.get_inventory() and len(qh.get_inventory()) == 4:
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, machine_id) and (datetime.datetime.now() - last_machine_click).total_seconds() > 45:
            osrs.move.fast_click(qh.get_inventory(enriched_bone_id))
            osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, machine_id)[0])
            last_machine_click = datetime.datetime.now()


def crafting_cape_tele():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        if qh.get_inventory() and qh.get_inventory('9781'):
            res = osrs.move.right_click_v5(qh.get_inventory('9781'), 'Teleport', in_inv=True)
            if res:
                return


def collect_enriched_bones():
    sluice_gate_id = '31436'
    rinsing_pool_id = '31437'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects(
        {'3689,3888,0', '3689,3891,0'},
        {sluice_gate_id, rinsing_pool_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    qh.set_inventory()
    qh.set_chat_options()
    start = None
    while True:
        qh.query_backend()
        if start and (datetime.datetime.now() - start).total_seconds() > 12:
            break
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, sluice_gate_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, sluice_gate_id)[0])
            if not start:
                start = datetime.datetime.now()

    while True:
        qh.query_backend()
        if qh.get_inventory(enriched_bone_id):
            osrs.clock.sleep_one_tick()
            osrs.clock.sleep_one_tick()
            osrs.keeb.press_key('space')
            return
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, rinsing_pool_id):
            osrs.move.fast_click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, rinsing_pool_id)[0])





bank_config = [
    {
        'id': [
            int(fossil_id)
        ],
        'quantity': 'All'
    }
]


script_config = {

    'intensity': 'low',
    'logout': False,
    'login': False,
}


def main():
    while True:
        osrs.bank.banking_handler({
            'search': [{'query': 'fossil', 'items': bank_config}]
        })
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        click_mounted_digsite_pendant()
        mushtree_to_meadow()
        osrs.game.break_manager_v4(script_config)
        run_to_hopper()
        add_fossils()
        enrich_bones()
        collect_enriched_bones()
        osrs.game.tele_home()
        click_mounted_digsite_pendant()
        add_bones_to_strange_machine()
        crafting_cape_tele()


main()
