import datetime
import osrs
from osrs.item_ids import ItemIDs


class PotConfig:
    def __init__(self, super_combat=False, ranging=False, magic=False, antipoision=False, antifire=False):
        self.SUPER_COMBATS = super_combat
        self.RANGING_POTION = ranging
        self.MAGIC_POTION = magic
        self.SUPER_ANTI_POISION = antipoision
        self.EXTENDED_ANTIFIRE = antifire

    def asdict(self):
        return {
            'SUPER_COMBATS': self.SUPER_COMBATS,
            'RANGING_POTION': self.RANGING_POTION,
            'MAGIC_POTION': self.MAGIC_POTION,
            'SUPER_ANTI_POISION': self.SUPER_ANTI_POISION,
            'EXTENDED_ANTIFIRE': self.EXTENDED_ANTIFIRE
        }


food_ids = [
    7946,  # monkfish
    3144,  # karambwan
    379,  # lobster
    385,  # shark
]

ANTIFIRE_VARBIT = '3981'

pot_matcher = {
    "SUPER_COMBATS": [
        ItemIDs.SUPER_COMBAT_POTION4.value,
        ItemIDs.SUPER_COMBAT_POTION3.value,
        ItemIDs.SUPER_COMBAT_POTION2.value,
        ItemIDs.SUPER_COMBAT_POTION1.value
    ],
    "RANGING_POTION": [
        ItemIDs.RANGING_POTION4.value,
        ItemIDs.RANGING_POTION3.value,
        ItemIDs.RANGING_POTION2.value,
        ItemIDs.RANGING_POTION1.value,
    ],
    "MAGIC_POTION": [
        ItemIDs.MAGIC_POTION4.value,
        ItemIDs.MAGIC_POTION3.value,
        ItemIDs.MAGIC_POTION2.value,
        ItemIDs.MAGIC_POTION1.value,
    ],
    "SUPER_ANTI_POISION": [
        ItemIDs.SUPERANTIPOISON4.value,
        ItemIDs.SUPERANTIPOISON3.value,
        ItemIDs.SUPERANTIPOISON2.value,
        ItemIDs.SUPERANTIPOISON1.value,
    ],
    "EXTENDED_ANTIFIRE": [
        ItemIDs.EXTENDED_ANTIFIRE4.value,
        ItemIDs.EXTENDED_ANTIFIRE3.value,
        ItemIDs.EXTENDED_ANTIFIRE2.value,
        ItemIDs.EXTENDED_ANTIFIRE1.value,
    ],
    "PRAYER": [
        ItemIDs.PRAYER_POTION4.value,
        ItemIDs.PRAYER_POTION3.value,
        ItemIDs.PRAYER_POTION2.value,
        ItemIDs.PRAYER_POTION1.value,
    ]
}

prayer_map = {
    'protect_melee': 4118,
    'protect_range': 4117,
    'protect_mage': 4116
}

prayer_map_widgets = {
    'protect_melee': '541,23',
    'protect_range': '541,22',
    'protect_mage': '541,21'
}


def find_next_target(npcs, min_monster_dist, max_monster_dist, ignore_interacting):
    res = False
    if not npcs:
        return False
    for npc in npcs:
        # always attack a monster if it is already attacking me and not dead
        if npc['health'] != 0 and 'interacting' in npc and 'GreazyDonkey' in npc['interacting']:
            print(f'attacking an npc that is already attacking me: {npc}')
            return npc
        if npc['health'] != 0 \
                and min_monster_dist <= npc['dist'] <= max_monster_dist \
                and (ignore_interacting or 'interacting' not in npc):
            if not res or npc['dist'] < res['dist']:
                res = npc
    return res


def prayer_handler(qh: osrs.queryHelper.QueryHelper, prayers):
    if not prayers:
        return
    for prayer in prayers:
        if prayer_map[prayer] not in qh.get_active_prayers():
            osrs.keeb.press_key('f5')
            osrs.clock.sleep_one_tick()
            qh.query_backend()
            osrs.move.fast_click(qh.get_widgets(prayer_map_widgets[prayer]))
    osrs.keeb.press_key('esc')


script_config = {
    'intensity': 'high',
    'login': False,
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def not_in_safe_spot(qh, ss_x, ss_y, ss_z):
    if ss_x == -1 or ss_y == -1 or ss_z == -1:
        return False
    if qh.get_player_world_location('x') == ss_x and qh.get_player_world_location('y') == ss_y:
        return False
    return True


def safe_spot_handler(qh, ss_x, ss_y, ss_z):
    # confirm we are safespotting
    while True:
        qh.query_backend()
        if not_in_safe_spot(qh, ss_x, ss_y, ss_z):
            print('out of safespot')
            if qh.get_tiles(f'{ss_x},{ss_y},{ss_z}') and osrs.move.is_clickable(qh.get_tiles(f'{ss_x},{ss_y},{ss_z}')):
                osrs.move.fast_click(qh.get_tiles(f'{ss_x},{ss_y},{ss_z}'))
        else:
            return


def food_handler(qh, min_health):
    if qh.get_skills('hitpoints')['boostedLevel'] < min_health:
        k = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), food_ids)
        if not k:
            return False
        osrs.move.click(k)
        osrs.clock.sleep_one_tick()
    return True


def pot_handler(qh: osrs.queryHelper.QueryHelper, pots):
    if 'SUPER_COMBATS' in pots \
            and pots['SUPER_COMBATS'] \
            and qh.get_skills('strength')['boostedLevel'] - qh.get_skills('strength')['level'] < 12:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_COMBATS'])
        if p:
            osrs.move.click(p)
        return True

    if 'RANGING_POTION' in pots \
            and pots['RANGING_POTION'] \
            and qh.get_skills('ranged')['boostedLevel'] - qh.get_skills('ranged')['level'] < 7:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['RANGING_POTION'])
        if p:
            osrs.move.click(p)
        return True

    if 'MAGIC_POTION' in pots \
            and pots['MAGIC_POTION'] \
            and qh.get_skills('magic')['boostedLevel'] - qh.get_skills('magic')['level'] < 3:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['MAGIC_POTION'])
        if p:
            osrs.move.click(p)
        return True

    if 'SUPER_ANTI_POISION' in pots \
            and pots['SUPER_ANTI_POISION'] \
            and int(qh.get_var_player('102')) > 0:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_ANTI_POISION'])
        if p:
            osrs.move.click(p)
        else:
            return False

    if 'EXTENDED_ANTIFIRE' in pots \
            and pots['EXTENDED_ANTIFIRE'] \
            and qh.get_varbit() == 0:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['EXTENDED_ANTIFIRE'])
        if p:
            osrs.move.click(p)
        else:
            return False
    if qh.get_skills('prayer')['boostedLevel'] < 15:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['PRAYER'])
        if p:
            osrs.move.click(p)
        else:
            return False
    return True


def hop_handler(qh: osrs.queryHelper.QueryHelper, pre_hop):
    # players is always minimum one since i am included
    if len(qh.get_players()) > 1:
        print('someone here')
        osrs.game.hop_worlds(pre_hop)


def main(npc_to_kill, pots, min_health, ss_x, ss_y, ss_z, min_monster_dist=0, max_monster_dist=999, hop=False, pre_hop=False, prayers=None, ignore_interacting=False):
    monster = npc_to_kill if type(npc_to_kill) is list else [npc_to_kill]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(monster)
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21'})
    qh.set_tiles({f'{ss_x},{ss_y},{ss_z}'})
    qh.set_player_world_location()
    qh.set_slayer()
    qh.set_var_player(['102'])
    qh.set_varbit(ANTIFIRE_VARBIT)
    qh.set_players()
    qh.set_active_prayers()
    while True:
        qh.query_backend()

        if not qh.get_slayer() or not qh.get_slayer()['monster']:
            print('task complete')
            return True

        if not qh.get_interating_with():
            targets = qh.get_npcs_by_name()
            c = find_next_target(targets, min_monster_dist, max_monster_dist, ignore_interacting)
            if c:
                osrs.move.fast_click(c)
                # sleep for one tick if i am trying to safespot so im not jumping in and out like a bot
                if -1 not in [ss_x, ss_y, ss_z]:
                    osrs.clock.sleep_one_tick()

        success = food_handler(qh, min_health)
        # Ran out of food, exit script
        if not success:
            print('failed to eat')
            return False

        safe_spot_handler(qh, ss_x, ss_y, ss_z)
        pot_success = pot_handler(qh, pots)
        if not pot_success:
            print('failed to pot up')
            return False

        prayer_handler(qh, prayers)

        # check if i leveled
        if qh.get_widgets('233,0'):
            for i in range(5):
                osrs.keeb.press_key('space')
                osrs.clock.sleep_one_tick()

        # dont try to tele unless im in safespot
        if not qh.get_interating_with():
            osrs.game.break_manager_v4(script_config)
            if hop:
                hop_handler(qh, pre_hop)

        osrs.player.toggle_run('on')
