import osrs
from osrs.item_ids import ItemIDs
from slayer import transport_functions
from combat import slayer_killer
from slayer.tasks import gear

varrock_tele_widget_id = '218,23'
supplies = [
        {
            'id': ItemIDs.COINS_995.value,
            'quantity': 'X',
            'amount': '200'
        },
        {
            'id': ItemIDs.NATURE_RUNE.value,
            'quantity': 'All'
        },
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.RUNE_POUCH.value,
        ItemIDs.KARAMJA_GLOVES_3.value,
        ItemIDs.DRAMEN_STAFF.value,
        {
            'id': ItemIDs.MONKFISH.value,
            'quantity': 'All'
        },
    ]
equipment = [
        ItemIDs.ABYSSAL_WHIP.value,
        ItemIDs.RUNE_DEFENDER.value,
        ItemIDs.BARROWS_GLOVES.value,
        ItemIDs.FIRE_CAPE.value,
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

pot_config = slayer_killer.PotConfig(super_atk=True, super_str=True)


def loot_builder():
    config = {
        'inv': [],
        'loot': []
    }

    item = osrs.loot.InvConfig(ItemIDs.MONKFISH.value, osrs.loot.monkfish_eval)
    config['inv'].append(item)

    item = osrs.loot.LootConfig(ItemIDs.RUNE_DAGGER.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.AIR_BATTLESTAFF.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.EARTH_BATTLESTAFF.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.BLACK_DHIDE_VAMBRACES.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.MYSTIC_AIR_STAFF.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.MYSTIC_EARTH_STAFF.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_DAGGER.value, 6, alch=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DUST_BATTLESTAFF.value, 6)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DRAGON_CHAINBODY.value, 8)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.DUST_RUNE.value, 8)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.EARTH_RUNE.value, 8)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.FIRE_RUNE.value, 8)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.CHAOS_RUNE.value, 8)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.SOUL_RUNE.value, 8)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.MITHRIL_BAR.value + 1, 8, stackable=True)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.COINS_995.value, 8, min_quantity=1000)
    config['loot'].append(item)
    item = osrs.loot.LootConfig(ItemIDs.ADAMANTITE_BAR.value + 1, 8)
    config['loot'].append(item)

    return config


def pre_log():
    osrs.clock.random_sleep(12, 13)


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
        while True:
            qh.query_backend()
            if qh.get_inventory(ItemIDs.DRAMEN_STAFF.value):
                osrs.move.click(qh.get_inventory(ItemIDs.DRAMEN_STAFF.value))
                break
        osrs.game.tele_home()
        osrs.game.click_restore_pool()
        osrs.game.tele_home_fairy_ring('biq')
        transport_functions.smoke_dungeon()
        qh.query_backend()
        while True:
            qh.query_backend()
            if qh.get_inventory(ItemIDs.ABYSSAL_WHIP.value):
                osrs.move.click(qh.get_inventory(ItemIDs.ABYSSAL_WHIP.value))
                break
        task_started = True
        finished = slayer_killer.main('dust devil', pot_config.asdict(), 35, hop=True, pre_hop=pre_log, loot_config=loot_builder())
        osrs.game.cast_spell(varrock_tele_widget_id)
        if finished:
            return
