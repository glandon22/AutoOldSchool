
# run to 2865,9827,1
# then exit
# 2134,9305,0
import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'


items = [
    ItemIDs.RUNE_POUCH.value,
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.AMULET_OF_FURY.value,
    ItemIDs.ARCHERS_RING.value,
    ItemIDs.AVAS_ACCUMULATOR.value,
    ItemIDs.SNAKESKIN_BOOTS.value,
    ItemIDs.ANTIDRAGON_SHIELD.value,
    ItemIDs.DRAGON_HUNTER_CROSSBOW.value,
    ItemIDs.VOID_RANGER_HELM.value,
    ItemIDs.VOID_KNIGHT_TOP.value,
    ItemIDs.VOID_KNIGHT_ROBE.value,
    ItemIDs.VOID_KNIGHT_GLOVES.value,
    {'id': ItemIDs.RUNITE_BOLTS.value, 'quantity': 'All'},
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
    {'id': ItemIDs.MONKFISH.value, 'quantity': '5'},
    ItemIDs.RANGING_POTION4.value,
    ItemIDs.RANGING_POTION4.value,
    ItemIDs.RANGING_POTION4.value,
]

equipment = [
    ItemIDs.DRAMEN_STAFF.value,
    ItemIDs.AMULET_OF_FURY.value,
    ItemIDs.ARCHERS_RING.value,
    ItemIDs.AVAS_ACCUMULATOR.value,
    ItemIDs.SNAKESKIN_BOOTS.value,
    ItemIDs.ANTIDRAGON_SHIELD.value,
    ItemIDs.VOID_RANGER_HELM.value,
    ItemIDs.VOID_KNIGHT_TOP.value,
    ItemIDs.VOID_KNIGHT_ROBE.value,
    ItemIDs.VOID_KNIGHT_GLOVES.value,
    ItemIDs.RUNITE_BOLTS.value,
]

banking_config = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer', 'items': items}]
}

pot_config = slayer_killer.PotConfig(ranging=True)


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
        osrs.game.cast_spell(fally_tele_widget_id)
        transport_functions.taverley_dungeon()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(ItemIDs.DRAGON_HUNTER_CROSSBOW.value))
        success = slayer_killer.main('baby black dragon', pot_config.asdict(), 35)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
