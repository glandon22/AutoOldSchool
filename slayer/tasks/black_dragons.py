
# run to 2865,9827,1
# then exit
# 2134,9305,0
import osrs

from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'


items = [
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.DRAMEN_STAFF,
    osrs.item_ids.AMULET_OF_FURY,
    osrs.item_ids.ARCHERS_RING,
    osrs.item_ids.AVAS_ACCUMULATOR,
    osrs.item_ids.SNAKESKIN_BOOTS,
    osrs.item_ids.ANTIDRAGON_SHIELD,
    osrs.item_ids.DRAGON_HUNTER_CROSSBOW,
    osrs.item_ids.VOID_RANGER_HELM,
    osrs.item_ids.VOID_KNIGHT_TOP,
    osrs.item_ids.VOID_KNIGHT_ROBE,
    osrs.item_ids.VOID_KNIGHT_GLOVES,
    {'id': osrs.item_ids.RUNITE_BOLTS, 'quantity': 'All'},
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
    {'id': osrs.item_ids.MONKFISH, 'quantity': '5'},
    osrs.item_ids.RANGING_POTION4,
    osrs.item_ids.RANGING_POTION4,
    osrs.item_ids.RANGING_POTION4,
]

equipment = [
    osrs.item_ids.DRAMEN_STAFF,
    osrs.item_ids.AMULET_OF_FURY,
    osrs.item_ids.ARCHERS_RING,
    osrs.item_ids.AVAS_ACCUMULATOR,
    osrs.item_ids.SNAKESKIN_BOOTS,
    osrs.item_ids.ANTIDRAGON_SHIELD,
    osrs.item_ids.VOID_RANGER_HELM,
    osrs.item_ids.VOID_KNIGHT_TOP,
    osrs.item_ids.VOID_KNIGHT_ROBE,
    osrs.item_ids.VOID_KNIGHT_GLOVES,
    osrs.item_ids.RUNITE_BOLTS,
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
        osrs.move.click(qh.get_inventory(osrs.item_ids.DRAGON_HUNTER_CROSSBOW))
        success = slayer_killer.main('baby black dragon', pot_config.asdict(), 35)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
