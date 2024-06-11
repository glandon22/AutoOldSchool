# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'


supplies = [
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': ItemIDs.PRAYER_POTION4.value,
        'quantity': '10'
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

    item = osrs.loot.LootConfig(ItemIDs.SNAPE_GRASS_SEED.value, 7)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.SNAPDRAGON_SEED.value, 17)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.TORSTOL_SEED.value, 17)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.WARRIOR_HELM.value, 17)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.ANCIENT_SHARD.value, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DARK_TOTEM_TOP.value, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DARK_TOTEM_BASE.value, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DARK_TOTEM_MIDDLE.value, 9)
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
