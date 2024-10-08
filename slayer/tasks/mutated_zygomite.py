import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
supplies = [
        osrs.item_ids.SUPER_COMBAT_POTION4,
        osrs.item_ids.RUNE_POUCH,
        osrs.item_ids.KARAMJA_GLOVES_4,
        {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
        {
            'id': osrs.item_ids.FUNGICIDE_SPRAY_10,
            'quantity': '5'
        },
        {
            'id': osrs.item_ids.MONKFISH,
            'quantity': 'All'
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
    {'id': osrs.item_ids.OSMUMTENS_FANG, 'consume': 'Wield'},
    {'id': osrs.item_ids.HOLY_BLESSING, 'consume': 'Equip'},
]

pot_config = slayer_killer.PotConfig(super_combat=True)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        qh.query_backend()
        print('starting function')
        if not task_started:
            bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('bks')
        transport_functions.zanaris_zygomites()
        qh.query_backend()
        while True:
            qh.query_backend()
            if qh.get_inventory(osrs.item_ids.OSMUMTENS_FANG):
                osrs.move.click(qh.get_inventory(osrs.item_ids.OSMUMTENS_FANG))
                break
        task_started = True
        finished = slayer_killer.main(['zygomite', 'fungi'], pot_config.asdict(), 35)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if finished:
            return

'''
run from fairy ring biq to 3309,3105,0
find npc id 17 and click need 200 gp for this carpet ride smh
click optino 3 to polli
in polli when coords 334 x 3366 :  2994 y 3012
click esc key
run to 3310,2959,0
find obj 6279 on tile 3310,2962,0
i dungeon when y greater than 9k
end func
'''