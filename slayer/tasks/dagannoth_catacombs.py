# 2134,9305,0
import datetime

import osrs

from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'


supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': osrs.item_ids.PRAYER_POTION4,
        'quantity': '10'
    },
]

equipment = [
        osrs.item_ids.RUNE_DEFENDER,
        osrs.item_ids.BARROWS_GLOVES,
        osrs.item_ids.FIRE_CAPE,
        osrs.item_ids.ABYSSAL_WHIP,
        osrs.item_ids.SLAYER_HELMET_I,
        osrs.item_ids.BRIMSTONE_RING,
        osrs.item_ids.DRAGON_BOOTS,
        osrs.item_ids.BANDOS_CHESTPLATE,
        osrs.item_ids.BANDOS_TASSETS,
        osrs.item_ids.AMULET_OF_FURY,
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
    osrs.player.turn_off_all_prayers()
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    last_tele_cast = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()
        if 1623 <= qh.get_player_world_location('x') <= 1656 and 3664 <= qh.get_player_world_location('y') <= 3684:
            break
        elif (datetime.datetime.now() - last_tele_cast).total_seconds() > 10:
            osrs.game.cast_spell('218,36')
            last_tele_cast = datetime.datetime.now()
    osrs.clock.random_sleep(10, 11)


def post_log():
    transport_functions.catacombs(1667, 9996)


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
    item = osrs.loot.LootConfig(osrs.item_ids.ANCIENT_SHARD, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DARK_TOTEM_TOP, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DARK_TOTEM_BASE, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(osrs.item_ids.DARK_TOTEM_MIDDLE, 9)
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
        transport_functions.catacombs(1667, 9996)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            ['dagannoth', 'dagannoth spawn'],
            pot_config.asdict(), 35,
            pre_hop=pre_log,
            hop=True,
            loot_config=loot_builder(),
            post_login=post_log,
            prayers=['protect_melee']
        )
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
        qh.query_backend()
