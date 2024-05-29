# 2134,9305,0
import datetime

import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'

supplies = [
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.RUNE_POUCH.value,
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
        ItemIDs.MONKFISH.value,
        ItemIDs.MONKFISH.value,
        {
            'id': ItemIDs.PRAYER_POTION4.value,
            'quantity': 'All'
        },
    ]

equipment = gear.melee_prayer['equipment']

banking_config_equipment = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'melee_prayer', 'items': equipment}]
}

banking_config_supplies = {
    'dump_inv': True,
    'dump_equipment': False,
    'search': [{'query': 'melee_prayer', 'items': supplies}]
}

pot_config = slayer_killer.PotConfig(super_str=True, super_atk=True)


def pre_log():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_tiles({'2885,9770,0'})
    qh.set_player_world_location()
    last_off_tile = datetime.datetime.now()
    while True:
        qh.query_backend()
        if qh.get_player_world_location('x') != 2885 \
                or qh.get_player_world_location('y') != 9770:
            last_off_tile = datetime.datetime.now()

        if qh.get_player_world_location('x') == 2885 \
                and qh.get_player_world_location('y') == 9770:
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 11:
                return
            if (datetime.datetime.now() - last_off_tile).total_seconds() > 3:
                osrs.player.turn_off_all_prayers()
        elif qh.get_tiles('2885,9770,0') and osrs.move.is_clickable(qh.get_tiles('2885,9770,0')):
            osrs.move.fast_click(qh.get_tiles('2885,9770,0'))
        else:
            osrs.move.follow_path(qh.get_player_world_location(), {'x': 2885, 'y': 9770, 'z': 0})


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
        osrs.game.cast_spell(fally_tele_widget_id)
        transport_functions.taverley_dungeon_black_demons()
        task_started = True
        success = slayer_killer.main('black demon', pot_config.asdict(), 35, prayers=['protect_melee'], hop=True, pre_hop=pre_log)
        osrs.player.turn_off_all_prayers()
        qh.query_backend()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
