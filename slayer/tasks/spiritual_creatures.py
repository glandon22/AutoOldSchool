'''

gwd entrance 26419 2917,3745,0
'''

# run to 2865,9827,1
# then exit
# 2134,9305,0
import datetime

import osrs
import osrs.move
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'
trollheim_tele_widget_id = '218,54'


supplies = [
    ItemIDs.SUPER_COMBAT_POTION4.value,
    ItemIDs.SUPER_COMBAT_POTION4.value,
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.SUPER_RESTORE4.value,
    {
        'id': [
            ItemIDs.SLAYER_RING_1.value,
            ItemIDs.SLAYER_RING_2.value,
            ItemIDs.SLAYER_RING_3.value,
            ItemIDs.SLAYER_RING_4.value,
            ItemIDs.SLAYER_RING_5.value,
            ItemIDs.SLAYER_RING_6.value,
            ItemIDs.SLAYER_RING_7.value,
            ItemIDs.SLAYER_RING_8.value,
        ],
        'quantity': '1'
    },
    {
        'id': ItemIDs.MONKFISH.value,
        'quantity': 'X',
        'amount': '9'
    },
    {
        'id': ItemIDs.PRAYER_POTION4.value,
        'quantity': 'All'
    },
]

equipment = [
    ItemIDs.ABYSSAL_WHIP.value,
    ItemIDs.HOLY_BLESSING.value,
    ItemIDs.RUNE_DEFENDER.value,
    ItemIDs.ARMADYL_BRACERS.value,
    ItemIDs.ZAMORAK_CLOAK.value,
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

pot_config = slayer_killer.PotConfig(super_combat=True)


def pre_log():
    safe_tile = {
        'x': 2898,
        'y': 5315,
        'z': 2
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
        osrs.clock.sleep_one_tick()
        osrs.game.cast_spell(trollheim_tele_widget_id)
        transport_functions.godwars_main_room()
        task_started = True
        while True:
            qh.query_backend()
            if qh.get_inventory(ItemIDs.SUPER_RESTORE4.value):
                osrs.move.fast_click(qh.get_inventory(ItemIDs.SUPER_RESTORE4.value))
            else:
                break
        success = slayer_killer.main('spiritual warrior', pot_config.asdict(), 35, prayers=['protect_melee'], ignore_interacting=True, pre_hop=pre_log)
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
