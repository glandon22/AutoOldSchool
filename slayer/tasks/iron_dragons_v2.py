# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'


supplies = [
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_ATTACK4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.SUPER_STRENGTH4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.KARAMJA_GLOVES_3.value,
    {
        'id': ItemIDs.MONKFISH.value,
        'quantity': '5'
    },
    {
        'id': ItemIDs.PRAYER_POTION4.value,
        'quantity': '10'
    },
    {
        'id': ItemIDs.NATURE_RUNE.value,
        'quantity': 'X',
        'amount': 50
    },
]

equipment = [*gear.melee_dragon['equipment'], ItemIDs.HOLY_BLESSING.value]

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


def pre_log():
    safe_tile = {
        'x': 2140,
        'y': 9298,
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


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.InvConfig(ItemIDs.MONKFISH.value, osrs.loot.monkfish_eval)
    config['inv'].append(item)

    item = osrs.loot.LootConfig(ItemIDs.DRAGON_PLATELEGS.value, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_PLATESKIRT.value, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.ADAMANT_2H_SWORD.value, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNE_MED_HELM.value, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNE_BATTLEAXE.value, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.RUNITE_LIMBS.value, 10, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRACONIC_VISAGE.value, 999)
    config['loot'].append(item)

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
        while True:
            qh.query_backend()
            if qh.get_inventory(ItemIDs.DRAMEN_STAFF.value):
                osrs.move.click(qh.get_inventory(ItemIDs.DRAMEN_STAFF.value))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('bjp')
        transport_functions.isle_of_souls_dungeon()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.DRAGON_HUNTER_LANCE.value))
        task_started = True
        success = slayer_killer.main('iron dragon', pot_config.asdict(), 35, prayers=['protect_melee'], hop=True, pre_hop=pre_log, loot_config=loot_builder())
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
