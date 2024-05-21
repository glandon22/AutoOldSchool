
# run to 2865,9827,1
# then exit
# 2134,9305,0
import osrs
import osrs.move
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer

varrock_tele_widget_id = '218,23'
fally_tele_widget_id = '218,29'


supplies = [
    ItemIDs.SUPER_COMBAT_POTION4.value,
    ItemIDs.SUPER_COMBAT_POTION4.value,
    ItemIDs.RUNE_POUCH.value,
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
    {
        'id': ItemIDs.MONKFISH.value,
        'quantity': 'All'
    },
]

equipment = [
    ItemIDs.DRAGON_HUNTER_LANCE.value,
    ItemIDs.RUNE_DEFENDER.value,
    ItemIDs.COMBAT_BRACELET.value,
    ItemIDs.OBSIDIAN_CAPE.value,
    ItemIDs.SLAYER_HELMET.value,
    ItemIDs.BRIMSTONE_RING.value,
    ItemIDs.DRAGON_BOOTS.value,
    ItemIDs.BANDOS_CHESTPLATE.value,
    ItemIDs.BANDOS_TASSETS.value,
    ItemIDs.AMULET_OF_FURY.value,
]

banking_config_equipment = {
    'dump_inv': True,
    'dump_equipment': True,
    'search': [{'query': 'slayer', 'items': equipment}]
}

banking_config_supplies = {
    'dump_inv': True,
    'dump_equipment': False,
    'search': [{'query': 'slayer', 'items': supplies}]
}

pot_config = slayer_killer.PotConfig(super_combat=True)


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    task_started = False
    while True:
        qh.query_backend()
        print('starting function')
        if not task_started:
            success = osrs.bank.banking_handler(banking_config_equipment)
            if not success:
                print('failed to withdraw equipment.')
                return False
            osrs.clock.sleep_one_tick()
            qh.query_backend()
            for item in qh.get_inventory():
                osrs.move.click(item)
            qh.query_backend()
        success = osrs.bank.banking_handler(banking_config_supplies)
        if not success:
            print('failed to withdraw supplies.')
            return False
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.clock.sleep_one_tick()
        osrs.game.cast_spell(fally_tele_widget_id)
        transport_functions.taverley_dungeon()
        task_started = True
        success = slayer_killer.main('baby black dragon', pot_config.asdict(), 35)
        osrs.game.cast_spell(varrock_tele_widget_id)
        if success:
            return True
