# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'

# for this one i dont want a slayer ring with only one charge,
# bc i tele to the cave, then to nieve after the task is done
supplies = [
        ItemIDs.SUPER_COMBAT_POTION4.value,
        ItemIDs.SUPER_COMBAT_POTION4.value,
        ItemIDs.RUNE_POUCH.value,
        {
            'id': [
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
            'quantity': '5'
        },
        {
            'id': ItemIDs.PRAYER_POTION4.value,
            'quantity': 'All'
        },
    ]
equipment = [
    ItemIDs.NOSE_PEG.value,
    ItemIDs.ABYSSAL_WHIP.value,
    ItemIDs.COMBAT_BRACELET.value,
    ItemIDs.BRIMSTONE_RING.value,
    ItemIDs.DRAGON_BOOTS.value,
    ItemIDs.MONKS_ROBE.value,
    ItemIDs.MONKS_ROBE_TOP.value,
    ItemIDs.AMULET_OF_FURY.value,
    ItemIDs.RUNE_DEFENDER.value,
    ItemIDs.HOLY_BLESSING.value,
    ItemIDs.ATTACK_CAPET.value,
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


def hop_logic():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'2471,9789,0'})
    qh.set_player_world_location()
    last_off_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') != 2471 \
                or qh.get_player_world_location('y') != 9789:
            last_off_tile = datetime.datetime.now()
            if qh.get_tiles('2471,9789,0'):
                osrs.move.fast_click(qh.get_tiles('2471,9789,0'))

        if qh.get_player_world_location('x') == 2471 \
                and qh.get_player_world_location('y') == 9789:
            osrs.player.turn_off_all_prayers()
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 11:
                return
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2471, 'y': 9789, 'z': 0})


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
        transport_functions.stronghold_slayer_dungeon_spectres()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'aberrant spectre',
            pot_config.asdict(),
            35, 15,
            hop=True, pre_hop=hop_logic,
            prayers=['protect_mage']
        )
        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
