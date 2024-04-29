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
    ]
}


def find_next_target(npcs, min_monster_dist, max_monster_dist):
    res = False
    for npc in npcs:
        if npc['health'] != 0 and min_monster_dist <= npc['dist'] <= max_monster_dist:
            if not res or npc['dist'] < res['dist']:
                res = npc
    return res


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
            and qh.get_skills('ranged')['RANGING_POTION'] - qh.get_skills('ranged')['level'] < 7:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['RANGING_POTION'])
        if p:
            osrs.move.click(p)
        return True

    if 'MAGIC_POTION' in pots \
            and pots['MAGIC_POTION'] \
            and qh.get_skills('magic')['MAGIC_POTION'] - qh.get_skills('magic')['level'] < 3:
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
        return False


def main(npc_to_kill, pots, min_health, ss_x, ss_y, ss_z, min_monster_dist=0, max_monster_dist=999):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([npc_to_kill])
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence'})
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_widgets({'233,0'})
    qh.set_tiles({f'{ss_x},{ss_y},{ss_z}'})
    qh.set_player_world_location()
    qh.set_slayer()
    qh.set_var_player(['102'])
    qh.set_varbit(ANTIFIRE_VARBIT)
    while True:
        qh.query_backend()

        if not qh.get_slayer() or not qh.get_slayer()['monster']:
            return True

        if not qh.get_interating_with():
            osrs.game.break_manager_v4(script_config)
            targets = qh.get_npcs_by_name()
            c = find_next_target(targets, min_monster_dist, max_monster_dist)
            if c:
                osrs.move.fast_click(c)

        success = food_handler(qh, min_health)
        # Ran out of food, exit script
        if not success:
            return False

        safe_spot_handler(qh, ss_x, ss_y, ss_z)
        pot_success = pot_handler(qh, pots)
        if not pot_success:
            return False

        # check if i leveled
        if qh.get_widgets('233,0'):
            for i in range(5):
                osrs.keeb.press_key('space')
                osrs.clock.sleep_one_tick()
