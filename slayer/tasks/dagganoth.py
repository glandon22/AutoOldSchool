# 2134,9305,0

import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts

varrock_tele_widget_id = '218,23'


supplies = [
    osrs.item_ids.WATERBIRTH_TELEPORT,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    },
]

equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.melee_str_chest,
    gear_loadouts.melee_str_legs,
    gear_loadouts.melee_boots,
    gear_loadouts.melee_str_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    gear_loadouts.high_def_weapon,
    gear_loadouts.prayer_ammo_slot
]

banking_config_equipment = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer', 'items': equipment}]
}

banking_config_supplies = {
    'dump_inv': True,
    'dump_equipment': False,
    'search': [{'query': 'slayer', 'items': supplies}]
}

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True)


def pre_log():
    stairs_out_id = '8966'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2441,10146,0'},
        {stairs_out_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_out_id):
            osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_out_id)[0])
            osrs.clock.sleep_one_tick()
        elif qh.get_player_world_location('y') < 9000:
            osrs.clock.random_sleep(11, 12)
            return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2444, 'y': 10146, 'z': 0})


def post_log():
    stairs_in_id = '8929'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects(
        {'2522,3738,0'},
        {stairs_in_id},
        osrs.queryHelper.ObjectTypes.GAME.value
    )
    while True:
        qh.query_backend()
        if qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_in_id):
            osrs.move.click(qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, stairs_in_id)[0])
            osrs.clock.sleep_one_tick()
        elif qh.get_player_world_location('y') > 9000:
            return


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.LootConfig(osrs.item_ids.SNAPE_GRASS_SEED, 7)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.SNAPDRAGON_SEED, 17)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.TORSTOL_SEED, 17)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.WARRIOR_HELM, 17)
    config['loot'].append(item)

    item = osrs.loot.InvConfig(osrs.item_ids.MONKFISH, osrs.loot.monkfish_eval)
    config['inv'].append(item)

    return config


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        qh.query_backend()
        print('starting function')
        if not task_started:
            success = osrs.bank.banking_handler(banking_config_equipment)
            if not success:
                print('failed to withdraw equipment.')
                return False
            osrs.clock.sleep_one_tick()
            qh.query_backend()
            for item in qh.get_inventory():
                osrs.move.click(item)
            qh.query_backend()
        success = osrs.bank.banking_handler(banking_config_supplies)
        if not success:
            print('failed to withdraw supplies.')
            return False
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        qh.query_backend()
        tab = qh.get_inventory(osrs.item_ids.WATERBIRTH_TELEPORT)
        if not tab:
            exit('missing tele tab')
        osrs.move.click(tab)
        transport_functions.waterbirth_dungeon()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            ['dagannoth', 'dagannoth spawn'],
            pot_config.asdict(), 35,
            attackable_area={'x_min': 2442, 'x_max': 2457, 'y_min': 10125, 'y_max': 10163},
            pre_hop=pre_log,
            post_login=post_log,
            loot_config=loot_builder()
        )
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
        qh.query_backend()
