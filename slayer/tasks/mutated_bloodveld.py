# 2134,9305,0
import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.utils import bank

varrock_tele_widget_id = '218,23'

# for this one i dont want a slayer ring with only one charge,
# bc i tele to the cave, then to nieve after the task is done
supplies = [
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.RUNE_POUCH.value,
        ItemIDs.KARAMJA_GLOVES_4.value,
        {
            'id': ItemIDs.NATURE_RUNE.value,
            'quantity': 'All'
        },
        {
            'id': [
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
        {
            'id': ItemIDs.PRAYER_POTION4.value,
            'quantity': '10'
        },
    ]


equipment = [
    {'id': ItemIDs.DRAGON_DEFENDER.value, 'consume': 'Wield'},
    {'id': ItemIDs.FIRE_CAPE.value, 'consume': 'Wear'},
    {'id': ItemIDs.SLAYER_HELMET_I.value, 'consume': 'Wear'},
    {'id': ItemIDs.BARROWS_GLOVES.value, 'consume': 'Wear'},
    {'id': ItemIDs.BRIMSTONE_RING.value, 'consume': 'Wear'},
    {'id': ItemIDs.DRAGON_BOOTS.value, 'consume': 'Wear'},
    {'id': ItemIDs.PROSELYTE_CUISSE.value, 'consume': 'Wear'},
    {'id': ItemIDs.PROSELYTE_HAUBERK.value, 'consume': 'Wear'},
    {'id': ItemIDs.AMULET_OF_FURY.value, 'consume': 'Wear'},
    {'id': ItemIDs.OSMUMTENS_FANG.value, 'consume': 'Wield'},
    {'id': ItemIDs.HOLY_BLESSING.value, 'consume': 'Equip'},
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def hop_logic():
    osrs.player.turn_off_all_prayers()
    osrs.clock.random_sleep(11, 11.1)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.catacombs(1693, 10015)
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'mutated bloodveld',
            pot_config.asdict(), 35,
            hop=True, pre_hop=hop_logic, prayers=['protect_melee']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
