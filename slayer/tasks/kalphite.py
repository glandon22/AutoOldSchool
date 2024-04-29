import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'


items = [
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.TOKTZKETXIL.value,
    ItemIDs.COMBAT_BRACELET.value,
    ItemIDs.OBSIDIAN_CAPE.value,
    ItemIDs.ABYSSAL_WHIP.value,
    ItemIDs.BLACK_MASK.value,
    ItemIDs.BRIMSTONE_RING.value,
    ItemIDs.DRAGON_BOOTS.value,
    ItemIDs.RUNE_PLATEBODY.value,
    ItemIDs.RUNE_PLATELEGS.value,
    ItemIDs.AMULET_OF_FURY.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.SUPERANTIPOISON4.value,
    ItemIDs.SUPERANTIPOISON4.value,
]

equipment = [
    ItemIDs.TOKTZKETXIL.value,
    ItemIDs.COMBAT_BRACELET.value,
    ItemIDs.OBSIDIAN_CAPE.value,
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.BLACK_MASK.value,
    ItemIDs.BRIMSTONE_RING.value,
    ItemIDs.DRAGON_BOOTS.value,
    ItemIDs.RUNE_PLATEBODY.value,
    ItemIDs.RUNE_PLATELEGS.value,
    ItemIDs.AMULET_OF_FURY.value,
]

banking_config = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer_melee', 'items': items}]
}

pot_config = slayer_killer.PotConfig(antipoision=True, super_combat=True)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        print('starting function')
        osrs.bank.banking_handler(banking_config)
        osrs.clock.sleep_one_tick()
        qh.query_backend()
        osrs.inv.power_drop(qh.get_inventory(), [], equipment)
        osrs.game.tele_home()
        osrs.clock.random_sleep(2, 2.1)
        osrs.game.tele_home_fairy_ring('biq')
        transport_functions.kalphite_layer()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.ABYSSAL_WHIP.value))
        finished = slayer_killer.main('kalphite worker', pot_config.asdict(), 35, -1, -1, -1)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if finished:
            return
