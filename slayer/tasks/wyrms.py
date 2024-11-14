# 2134,9305,0
import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank


varrock_tele_widget_id = '218,23'

weapon = gear_loadouts.dragon_melee_weapon
supplies = [
    {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_ATTACK4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.SUPER_STRENGTH4,
    osrs.item_ids.RUNE_POUCH,
    osrs.item_ids.KARAMJA_GLOVES_3,
    {
        'id': [
            osrs.item_ids.PRAYER_POTION4
        ],
        'quantity': '5'
    },
    {
        'id': osrs.item_ids.NATURE_RUNE,
        'quantity': 'All'
    },
    {
        'id': osrs.item_ids.MONKFISH,
        'quantity': 'All'
    },
]

equipment = [
    gear_loadouts.slayer_helm,
    gear_loadouts.melee_necklace,
    gear_loadouts.melee_str_chest,
    gear_loadouts.melee_str_legs,
    gear_loadouts.melee_boots,
    gear_loadouts.dragon_melee_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    weapon,
    gear_loadouts.prayer_ammo_slot
]


pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    osrs.player.turn_off_all_prayers()
    osrs.clock.random_sleep(12, 12.1)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('cir')
        transport_functions.mount_karuulm_wyrms()
        qh.query_backend()
        osrs.move.click(qh.get_inventory(weapon['id']))
        task_started = True
        success = slayer_killer.main(
            'wyrm', pot_config.asdict(), 35, pre_hop=pre_log, prayers=['protect_mage'],
            attackable_area={'x_min': 1251, 'x_max': 1276, 'y_min': 10147, 'y_max': 10161},
        )
        qh.query_backend()
        osrs.player.turn_off_all_prayers()
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
