# 2134,9305,0
import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
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
        osrs.item_ids.KARAMJA_GLOVES_3,
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
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.prayer_top,
    gear_loadouts.prayer_bottom,
    gear_loadouts.melee_boots,
    gear_loadouts.melee_str_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    gear_loadouts.high_def_weapon,
    gear_loadouts.prayer_ammo_slot
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
        transport_functions.stronghold_slayer_cave(2488, 9823)
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


def mory():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        transport_functions.mory_slayer_tower('bloodvelds')
        qh.query_backend()
        task_started = True
        success = slayer_killer.main(
            'bloodveld',
            pot_config.asdict(), 35,
            pre_hop=hop_logic, prayers=['protect_melee']
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
