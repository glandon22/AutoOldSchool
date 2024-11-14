import osrs

from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'


items = [
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.DRAMEN_STAFF,
    osrs.item_ids.OCCULT_NECKLACE,
    osrs.item_ids.SEERS_RING,
    osrs.item_ids.FIRE_CAPE,
    osrs.item_ids.WIZARD_BOOTS,
    osrs.item_ids.ANTIDRAGON_SHIELD,
    osrs.item_ids.TRIDENT_OF_THE_SWAMP,
    osrs.item_ids.VOID_MAGE_HELM,
    osrs.item_ids.VOID_KNIGHT_TOP,
    osrs.item_ids.VOID_KNIGHT_ROBE,
    osrs.item_ids.VOID_KNIGHT_GLOVES,
    osrs.item_ids.MONKFISH,
    osrs.item_ids.MONKFISH,
    osrs.item_ids.MONKFISH,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    osrs.item_ids.EXTENDED_ANTIFIRE4,
    {
        'id': [
            osrs.item_ids.SLAYER_RING_1,
            osrs.item_ids.SLAYER_RING_2,
            osrs.item_ids.SLAYER_RING_3,
            osrs.item_ids.SLAYER_RING_4,
            osrs.item_ids.SLAYER_RING_5,
            osrs.item_ids.SLAYER_RING_6,
            osrs.item_ids.SLAYER_RING_7,
            osrs.item_ids.SLAYER_RING_8,
        ],
        'quantity': '1'
    },

]

equipment = [
    osrs.item_ids.DRAMEN_STAFF,
    osrs.item_ids.OCCULT_NECKLACE,
    osrs.item_ids.SEERS_RING,
    osrs.item_ids.FIRE_CAPE,
    osrs.item_ids.WIZARD_BOOTS,
    osrs.item_ids.ANTIDRAGON_SHIELD,
    osrs.item_ids.VOID_MAGE_HELM,
    osrs.item_ids.VOID_KNIGHT_TOP,
    osrs.item_ids.VOID_KNIGHT_ROBE,
    osrs.item_ids.VOID_KNIGHT_GLOVES,
]

banking_config = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'metal_dragons', 'items': items}]
}

pot_config = slayer_killer.PotConfig(antifire=True)


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
        osrs.game.tele_home_fairy_ring('bjp')
        transport_functions.isle_of_souls_dungeon()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(osrs.item_ids.TRIDENT_OF_THE_SWAMP))
        success = slayer_killer.main('iron dragon', pot_config.asdict(), 35, 2145, 9296, 0, 3, 5)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
