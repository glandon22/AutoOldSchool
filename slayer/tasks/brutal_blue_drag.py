# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'


supplies = [
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': ItemIDs.PRAYER_POTION4.value,
        'quantity': '10'
    },
    {
        'id': ItemIDs.NATURE_RUNE.value,
        'quantity': 'All'
    },
    {
        'id': ItemIDs.MONKFISH.value,
        'quantity': 'All'
    },
]

equipment = gear.melee_dragon['equipment']

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

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True, antifire=True)


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.LootConfig(ItemIDs.ADAMANT_PLATELEGS.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNE_LONGSWORD.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.BLUE_DHIDE_BODY.value, 5, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_DAGGER.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_LONGSWORD.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_MED_HELM.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNE_FULL_HELM.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNE_PLATEBODY.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.CHAOS_RUNE.value, 3, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DEATH_RUNE.value, 3, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.LAW_RUNE.value, 3, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_DART_TIP.value, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_ARROWTIPS.value, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNITE_ORE.value + 1, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_JAVELIN_HEADS.value, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRACONIC_VISAGE.value, 93)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.ANCIENT_SHARD.value, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DARK_TOTEM_TOP.value, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DARK_TOTEM_BASE.value, 9)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DARK_TOTEM_MIDDLE.value, 9)
    config['loot'].append(item)

    return config


def pre_log():
    safe_tile = {
        'x': 1638,
        'y': 10074,
        'z': 0
    }
    safe_tile_string = f'{safe_tile["x"]},{safe_tile["y"]},{safe_tile["z"]}'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({safe_tile_string})
    qh.set_player_world_location()
    last_off_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') != safe_tile["x"] \
                or qh.get_player_world_location('y') != safe_tile["y"]:
            last_off_tile = datetime.datetime.now()

        if qh.get_player_world_location('x') == safe_tile["x"] \
                and qh.get_player_world_location('y') == safe_tile["y"]:
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 11:
                return
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 3:
                osrs.player.turn_off_all_prayers()
        elif qh.get_tiles(safe_tile_string):
            osrs.move.fast_click(qh.get_tiles(safe_tile_string))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), safe_tile)


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
        transport_functions.catacombs(1638, 10074)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'brutal blue dragon', pot_config.asdict(), 35,
            hop=True, pre_hop=pre_log, loot_config=loot_builder(), prayers=['protect_mage']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
