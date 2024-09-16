# 2134,9305,0
import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'

# for this one i dont want a slayer ring with only one charge,
# bc i tele to the cave, then to nieve after the task is done
supplies = [
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.RUNE_POUCH,
        osrs.item_ids.KARAMJA_GLOVES_4,
        {
            'id': osrs.item_ids.NATURE_RUNE,
            'quantity': 'All'
        },
        {
            'id': [
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
        {
            'id': osrs.item_ids.PRAYER_POTION4,
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
    {'id': osrs.item_ids.PROSELYTE_CUISSE, 'consume': 'Wear'},
    {'id': osrs.item_ids.PROSELYTE_HAUBERK, 'consume': 'Wear'},
    {'id': osrs.item_ids.AMULET_OF_FURY, 'consume': 'Wear'},
    {'id': osrs.item_ids.OSMUMTENS_FANG, 'consume': 'Wield'},
    {'id': osrs.item_ids.HOLY_BLESSING, 'consume': 'Equip'},
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def hop_logic():
    osrs.clock.random_sleep(11, 11.1)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.stronghold_slayer_dungeon_bloodvelds()
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'bloodveld',
            pot_config.asdict(), 35,
            attackable_area={'x_min': 2481, 'x_max': 2494, 'y_min': 9814, 'y_max': 9832},
            hop=True, pre_hop=hop_logic, prayers=['protect_melee']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
