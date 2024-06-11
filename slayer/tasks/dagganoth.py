# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'


supplies = [
    ItemIDs.WATERBIRTH_TELEPORT.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': ItemIDs.MONKFISH.value,
        'quantity': 'All'
    },
]

equipment = [
        ItemIDs.RUNE_DEFENDER.value,
        ItemIDs.BARROWS_GLOVES.value,
        ItemIDs.FIRE_CAPE.value,
        ItemIDs.ABYSSAL_WHIP.value,
        ItemIDs.SLAYER_HELMET.value,
        ItemIDs.BRIMSTONE_RING.value,
        ItemIDs.DRAGON_BOOTS.value,
        ItemIDs.BANDOS_CHESTPLATE.value,
        ItemIDs.BANDOS_TASSETS.value,
        ItemIDs.AMULET_OF_FURY.value,
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

    item = osrs.loot.LootConfig(ItemIDs.SNAPE_GRASS_SEED.value, 7)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.SNAPDRAGON_SEED.value, 17)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.TORSTOL_SEED.value, 17)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.WARRIOR_HELM.value, 17)
    config['loot'].append(item)

    item = osrs.loot.InvConfig(ItemIDs.MONKFISH.value, osrs.loot.monkfish_eval)
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
        tab = qh.get_inventory(ItemIDs.WATERBIRTH_TELEPORT.value)
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
