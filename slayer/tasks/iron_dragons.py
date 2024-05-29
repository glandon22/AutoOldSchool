import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'


items = [
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.OCCULT_NECKLACE.value,
    ItemIDs.SEERS_RING.value,
    ItemIDs.FIRE_CAPE.value,
    ItemIDs.WIZARD_BOOTS.value,
    ItemIDs.ANTIDRAGON_SHIELD.value,
    ItemIDs.TRIDENT_OF_THE_SWAMP.value,
    ItemIDs.VOID_MAGE_HELM.value,
    ItemIDs.VOID_KNIGHT_TOP.value,
    ItemIDs.VOID_KNIGHT_ROBE.value,
    ItemIDs.VOID_KNIGHT_GLOVES.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.MONKFISH.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
    ItemIDs.EXTENDED_ANTIFIRE4.value,
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

]

equipment = [
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.OCCULT_NECKLACE.value,
    ItemIDs.SEERS_RING.value,
    ItemIDs.FIRE_CAPE.value,
    ItemIDs.WIZARD_BOOTS.value,
    ItemIDs.ANTIDRAGON_SHIELD.value,
    ItemIDs.VOID_MAGE_HELM.value,
    ItemIDs.VOID_KNIGHT_TOP.value,
    ItemIDs.VOID_KNIGHT_ROBE.value,
    ItemIDs.VOID_KNIGHT_GLOVES.value,
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
        osrs.move.click(qh.get_inventory(ItemIDs.TRIDENT_OF_THE_SWAMP.value))
        success = slayer_killer.main('iron dragon', pot_config.asdict(), 35, 2145, 9296, 0, 3, 5)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
