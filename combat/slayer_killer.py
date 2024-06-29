import datetime

import pyautogui
from matplotlib.path import Path
import osrs
from osrs.item_ids import ItemIDs


class PotConfig:
    def __init__(self, super_combat=False, ranging=False, magic=False, antipoision=False, antifire=False,
                 super_str=False, super_atk=False, super_def=False):
        self.SUPER_COMBATS = super_combat
        self.RANGING_POTION = ranging
        self.MAGIC_POTION = magic
        self.SUPER_ANTI_POISION = antipoision
        self.EXTENDED_ANTIFIRE = antifire
        self.SUPER_ATK = super_atk
        self.SUPER_STR = super_str
        self.SUPER_DEF = super_def

    def asdict(self):
        return {
            'SUPER_COMBATS': self.SUPER_COMBATS,
            'RANGING_POTION': self.RANGING_POTION,
            'MAGIC_POTION': self.MAGIC_POTION,
            'SUPER_ANTI_POISION': self.SUPER_ANTI_POISION,
            'EXTENDED_ANTIFIRE': self.EXTENDED_ANTIFIRE,
            'SUPER_ATTACK': self.SUPER_ATK,
            'SUPER_STRENGTH': self.SUPER_STR,
            'SUPER_DEFENCE': self.SUPER_DEF
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
    "SUPER_ATTACK": [
        ItemIDs.SUPER_ATTACK4.value,
        ItemIDs.SUPER_ATTACK3.value,
        ItemIDs.SUPER_ATTACK2.value,
        ItemIDs.SUPER_ATTACK1.value,
    ],
    "SUPER_STRENGTH": [
        ItemIDs.SUPER_STRENGTH4.value,
        ItemIDs.SUPER_STRENGTH3.value,
        ItemIDs.SUPER_STRENGTH2.value,
        ItemIDs.SUPER_STRENGTH1.value,
    ],
    "SUPER_DEFENCE": [
        ItemIDs.SUPER_DEFENCE4.value,
        ItemIDs.SUPER_DEFENCE3.value,
        ItemIDs.SUPER_DEFENCE2.value,
        ItemIDs.SUPER_DEFENCE1.value,
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


random_event_npcs_to_ignore = [
    6747, # beekeeper
    5426, # arnav
    12551, 12552, # count check
    307, 314, # jekyll
    322, # drunken dwarf
    6749, # dunce
    390, 6754, # evil bob
    6744, # flippa
    6748, # forester
    5429, 5430, 5431, 5432, 312, 5434, 5435, # frogs
    326, 327, # genie
    5438, 5441, # giles
    6746, # leo
    5437, 5440, # miles
    6750, 6751, 6752, 6753, # mys old man
    5436, 5439, # niles
    380, # pillory
    6738, # postie
    6755, # quiz master
    375, 376, # turpentine
    5510, # sandwich
    6743, # sargeant damien
    10, # Death spawn from nechryael. not a random but whatever
]


def find_next_target(npcs, monster, ignore_interacting, attackable_area):
    def target_filter_function(npc):
        print('cblvl', npc['cbLvl'])
        if int(npc['id']) in random_event_npcs_to_ignore:
            return False
        # If an attackable area is configured, ensure that this monster is within it
        if attackable_area:
            in_area = Path([
                (attackable_area['x_max'], attackable_area['y_max']),
                (attackable_area['x_max'], attackable_area['y_min']),
                (attackable_area['x_min'], attackable_area['y_max']),
                (attackable_area['x_min'], attackable_area['y_min'])
            ], closed=True).contains_point((npc['x_coord'], npc['y_coord']))
            if not in_area:
                print(
                    (attackable_area['x_max'], attackable_area['y_max']),
                    (attackable_area['x_max'], attackable_area['y_min']),
                    (attackable_area['x_min'], attackable_area['y_max']),
                    (attackable_area['x_min'], attackable_area['y_min'])
                )
                print(npc)
            if not in_area:
                return False
        # Ignore any NPC that is already dead!
        if npc['health'] == 0:
            return False
        if not npc['cbLvl'] or npc['cbLvl'] <= 0:
            return False
        # If this monster is already interacting with someone other than me,
        # check to see if i have ignore_interacting set. If not, ignore this monster
        if 'interacting' in npc and 'GreazyDonkey' not in npc['interacting']:
            if not ignore_interacting:

                return False
        return True
    # remove monsters that are out of bounds, dead, fighting someone else or not what i want to kill
    filtered_npcs = list(filter(target_filter_function, npcs))
    if len(filtered_npcs) == 0:
        print('could not find a suitable monster on first pass')
        return False
    monster_attacking_me = list(filter(lambda npc: 'interacting' in npc and 'GreazyDonkey' in npc['interacting'], filtered_npcs))
    # there is a monster already attacking me - kill it
    if len(monster_attacking_me) > 0:
        print('there is a monster already attacking - targeting it')
        return sorted(monster_attacking_me, key=lambda npc: npc['dist'])[0]
    # now filter out any monsters that are not my task since i have confirmed no other monsters are attacking me
    final_filter_list = list(filter(lambda npc: npc['name'].lower() in monster, filtered_npcs))
    if len(final_filter_list) == 0:
        return False
    sorted_npcs = sorted(final_filter_list, key=lambda npc: npc['dist'])
    return sorted_npcs[0]


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

    if 'SUPER_ATTACK' in pots \
            and pots['SUPER_ATTACK'] \
            and qh.get_skills('attack')['boostedLevel'] - qh.get_skills('attack')['level'] < 12:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_ATTACK'])
        if p:
            osrs.move.click(p)

    if 'SUPER_STRENGTH' in pots \
            and pots['SUPER_STRENGTH'] \
            and qh.get_skills('strength')['boostedLevel'] - qh.get_skills('strength')['level'] < 12:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_STRENGTH'])
        if p:
            osrs.move.click(p)

    if 'SUPER_DEFENCE' in pots \
            and pots['SUPER_DEFENCE'] \
            and qh.get_skills('defence')['boostedLevel'] - qh.get_skills('defence')['level'] < 12:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_DEFENCE'])
        if p:
            osrs.move.click(p)

    if 'RANGING_POTION' in pots \
            and pots['RANGING_POTION'] \
            and qh.get_skills('ranged')['boostedLevel'] - qh.get_skills('ranged')['level'] < 7:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['RANGING_POTION'])
        if p:
            osrs.move.click(p)

    if 'MAGIC_POTION' in pots \
            and pots['MAGIC_POTION'] \
            and qh.get_skills('magic')['boostedLevel'] - qh.get_skills('magic')['level'] < 3:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['MAGIC_POTION'])
        if p:
            osrs.move.click(p)

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


def hop_handler(qh: osrs.queryHelper.QueryHelper, pre_hop, last_seen, post_login=None):
    # players is always minimum one since i am included
    if qh.get_players() and len(qh.get_players()) > 1:
        print('someone here', qh.get_players())
        if last_seen is None:
            return datetime.datetime.now()
        elif (datetime.datetime.now() - last_seen).total_seconds() > 10:
            osrs.game.hop_worlds(pre_hop)
            if post_login:
                post_login()
            return None
        else:
            return last_seen
    return None


def main(
    npc_to_kill, pots, min_health, hop=False,
    pre_hop=False, prayers=None, ignore_interacting=False,
    attackable_area=None,
    post_login=None, loot_config=None
):
    player_last_seen = None
    monster = npc_to_kill if type(npc_to_kill) is list else [npc_to_kill]
    monster = [item.lower() for item in monster]
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name([])
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
    qh.set_inventory()
    qh.set_interating_with()
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62'})
    qh.set_player_world_location()
    qh.set_slayer()
    qh.set_var_player(['102'])
    qh.set_varbit(ANTIFIRE_VARBIT)
    qh.set_players()
    qh.set_active_prayers()

    script_config = {
        'intensity': 'high',
        'login': False,
        'logout': lambda: osrs.clock.random_sleep(11, 14),
    }

    if pre_hop:
        script_config['logout'] = pre_hop
    if post_login:
        script_config['login'] = post_login

    loot_handler = osrs.loot.Loot()
    if loot_config:
        for item in loot_config['inv']:
            loot_handler.add_inv_config_item(item)
        for item in loot_config['loot']:
            loot_handler.add_item(item)

    last_interacting = datetime.datetime.now() - datetime.timedelta(hours=1)
    while True:
        qh.query_backend()

        # Pull up inv if i am on another tab
        if qh.get_widgets('161,62') and qh.get_widgets('161,62')['spriteID'] != 1030:
            print('jere', qh.get_widgets('161,62'))
            osrs.keeb.press_key('esc')

        if not qh.get_slayer() or not qh.get_slayer()['monster']:
            print('task complete')
            return True

        if not qh.get_interating_with():
            # Look for any loot, and we dont want to count time looking for loot as time out of combat bc it
            # leads to weird behavior
            loot_handler.retrieve_loot(12)
            qh.query_backend()

            config = osrs.game.break_manager_v4(script_config)

            if hop:
                player_last_seen = hop_handler(qh, pre_hop, player_last_seen, post_login)

            if (datetime.datetime.now() - last_interacting).total_seconds() > 2:
                monster_search_start = datetime.datetime.now()
                qh2 = osrs.queryHelper.QueryHelper()
                qh2.set_npcs_by_name([])
                qh2.set_interating_with()
                while True:
                    qh2.query_backend()
                    if qh2.get_interating_with():
                        last_interacting = datetime.datetime.now()
                        break
                    targets = qh2.get_npcs_by_name()
                    c = find_next_target(targets, monster, ignore_interacting, attackable_area)
                    if c:
                        osrs.move.fast_click(c)
                        pyautogui.click()
                    elif (datetime.datetime.now() - monster_search_start).total_seconds() > 7:
                        break
                continue

        success = food_handler(qh, min_health)
        # Ran out of food, exit script
        if not success:
            print('failed to eat')
            return False

        pot_success = pot_handler(qh, pots)
        if not pot_success:
            print('failed to pot up')
            return False

        prayer_handler(qh, prayers)

        osrs.player.toggle_run('on')
