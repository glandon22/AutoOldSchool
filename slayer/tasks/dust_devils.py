import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'
supplies = [
        {
            'id': osrs.item_ids.COINS_995,
            'quantity': 'X',
            'amount': '200'
        },
        {
            'id': osrs.item_ids.NATURE_RUNE,
            'quantity': 'All'
        },
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.RUNE_POUCH,
        osrs.item_ids.KARAMJA_GLOVES_3,
        osrs.item_ids.DRAMEN_STAFF,
        {
            'id': osrs.item_ids.MONKFISH,
            'quantity': 'All'
        },
    ]
equipment = [
        osrs.item_ids.ABYSSAL_WHIP,
        osrs.item_ids.RUNE_DEFENDER,
        osrs.item_ids.BARROWS_GLOVES,
        osrs.item_ids.FIRE_CAPE,
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

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    osrs.clock.random_sleep(12, 13)


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
            if qh.get_inventory(osrs.item_ids.DRAMEN_STAFF):
                osrs.move.click(qh.get_inventory(osrs.item_ids.DRAMEN_STAFF))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('biq')
        transport_functions.smoke_dungeon()
        qh.query_backend()
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.ABYSSAL_WHIP):
                osrs.move.click(qh.get_inventory(osrs.item_ids.ABYSSAL_WHIP))
                break
        task_started = True
        finished = slayer_killer.main('dust devil', pot_config.asdict(), 35, pre_hop=pre_log)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if finished:
            return
