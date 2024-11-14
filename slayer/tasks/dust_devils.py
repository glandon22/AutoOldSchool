import osrs

from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear_loadouts
from slayer.utils import bank

varrock_tele_widget_id = '218,23'
weapon = gear_loadouts.high_def_weapon
supplies = [
        {
            'id': osrs.item_ids.COINS_995,
            'quantity': 'X',
            'amount': '200'
        },
        {
            'id': osrs.item_ids.NATURE_RUNE,
            'quantity': 'All'
        },
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.RUNE_POUCH,
        osrs.item_ids.KARAMJA_GLOVES_3,
        {'id': osrs.item_ids.DRAMEN_STAFF, 'consume': 'Wield'},
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
    gear_loadouts.melee_str_shield,
    gear_loadouts.melee_cape,
    gear_loadouts.melee_gloves,
    gear_loadouts.melee_ring,
    weapon,
    gear_loadouts.prayer_ammo_slot
]

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def pre_log():
    osrs.clock.random_sleep(12, 13)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        bank(qh, task_started, equipment, supplies)
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('biq')
        transport_functions.smoke_dungeon()
        qh.query_backend()
        while True:
            qh.query_backend()
            if qh.get_inventory(weapon['id']):
                osrs.move.click(qh.get_inventory(weapon['id']))
                break
        task_started = True
        finished = slayer_killer.main('dust devil', pot_config.asdict(), 35, pre_hop=pre_log)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if finished:
            return
