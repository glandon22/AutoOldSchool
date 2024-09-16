import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
supplies = [
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_4,
    osrs.item_ids.DRAMEN_STAFF,
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': '10'
    },
]
equipment = [
    {'id': osrs.item_ids.DRAGON_DEFENDER, 'consume': 'Wield'},
    {'id': osrs.item_ids.FIRE_CAPE, 'consume': 'Wear'},
    {'id': osrs.item_ids.SLAYER_HELMET_I, 'consume': 'Wear'},
    {'id': osrs.item_ids.BARROWS_GLOVES, 'consume': 'Wear'},
    {'id': osrs.item_ids.BRIMSTONE_RING, 'consume': 'Wear'},
    {'id': osrs.item_ids.DRAGON_BOOTS, 'consume': 'Wear'},
    {'id': osrs.item_ids.BANDOS_CHESTPLATE, 'consume': 'Wear'},
    {'id': osrs.item_ids.BANDOS_TASSETS, 'consume': 'Wear'},
    {'id': osrs.item_ids.AMULET_OF_FURY, 'consume': 'Wear'},
    {'id': osrs.item_ids.ABYSSAL_WHIP},
    {'id': osrs.item_ids.HOLY_BLESSING, 'consume': 'Equip'},
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
]

pot_config = slayer_killer.PotConfig(super_combat=True)


def pre_log():
    osrs.clock.random_sleep(12, 13)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        qh.query_backend()
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('biq')
        transport_functions.kalphite_layer()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(osrs.item_ids.ABYSSAL_WHIP))
        task_started = True
        finished = slayer_killer.main('kalphite worker', pot_config.asdict(), 35, hop=True, pre_hop=pre_log)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if finished:
            return
