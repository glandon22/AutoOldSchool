from datetime import datetime

import pyautogui

import osrs

pot_handler_required_prayer_widgets = {'233,0', '541,23', '541,22', '541,21', '161,62', '541,25'}
pot_handler_required_skills = {'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'}


class PotConfig:
    def __init__(self, super_combat=False, ranging=False, magic=False, antipoision=False, antifire=False,
                 super_str=False, super_atk=False, super_def=False, antivenom=False, prayer=False,
                 superantifire=False, stamina=False
                 ):
        self.SUPER_COMBATS = super_combat
        self.RANGING_POTION = ranging
        self.MAGIC_POTION = magic
        self.SUPER_ANTI_POISION = antipoision
        self.ANTIFIRE = antifire
        self.SUPER_ANTIFIRE = superantifire
        self.SUPER_ATK = super_atk
        self.SUPER_STR = super_str
        self.SUPER_DEF = super_def
        self.ANTIVENOM = antivenom
        self.PRAYER = prayer
        self.STAMINA = stamina

    def asdict(self):
        return {
            'SUPER_COMBATS': self.SUPER_COMBATS,
            'RANGING_POTION': self.RANGING_POTION,
            'MAGIC_POTION': self.MAGIC_POTION,
            'SUPER_ANTI_POISION': self.SUPER_ANTI_POISION,
            'ANTIFIRE': self.ANTIFIRE,
            'SUPER_ANTIFIRE': self.SUPER_ANTIFIRE,
            'SUPER_ATTACK': self.SUPER_ATK,
            'SUPER_STRENGTH': self.SUPER_STR,
            'SUPER_DEFENCE': self.SUPER_DEF,
            'ANTIVENOM': self.ANTIVENOM,
            'PRAYER': self.PRAYER,
            'STAMINA': self.STAMINA
        }


food_ids = [
    7946,  # monkfish
    3144,  # karambwan
    379,  # lobster
    385,  # shark
    osrs.item_ids.PEACH
]

pot_matcher = {
    "STAMINA": [
        osrs.item_ids.STAMINA_POTION1,
        osrs.item_ids.STAMINA_POTION2,
        osrs.item_ids.STAMINA_POTION3,
        osrs.item_ids.STAMINA_POTION4,
    ],
    "SUPER_COMBATS": [
        osrs.item_ids.SUPER_COMBAT_POTION4,
        osrs.item_ids.SUPER_COMBAT_POTION3,
        osrs.item_ids.SUPER_COMBAT_POTION2,
        osrs.item_ids.SUPER_COMBAT_POTION1,
    ],
    "SUPER_ATTACK": [
        osrs.item_ids.SUPER_ATTACK4,
        osrs.item_ids.SUPER_ATTACK3,
        osrs.item_ids.SUPER_ATTACK2,
        osrs.item_ids.SUPER_ATTACK1,
    ],
    "SUPER_STRENGTH": [
        osrs.item_ids.SUPER_STRENGTH4,
        osrs.item_ids.SUPER_STRENGTH3,
        osrs.item_ids.SUPER_STRENGTH2,
        osrs.item_ids.SUPER_STRENGTH1,
    ],
    "SUPER_DEFENCE": [
        osrs.item_ids.SUPER_DEFENCE4,
        osrs.item_ids.SUPER_DEFENCE3,
        osrs.item_ids.SUPER_DEFENCE2,
        osrs.item_ids.SUPER_DEFENCE1,
    ],
    "RANGING_POTION": [
        osrs.item_ids.RANGING_POTION4,
        osrs.item_ids.RANGING_POTION3,
        osrs.item_ids.RANGING_POTION2,
        osrs.item_ids.RANGING_POTION1,
        osrs.item_ids.DIVINE_RANGING_POTION4,
        osrs.item_ids.DIVINE_RANGING_POTION3,
        osrs.item_ids.DIVINE_RANGING_POTION2,
        osrs.item_ids.DIVINE_RANGING_POTION1,
    ],
    "MAGIC_POTION": [
        osrs.item_ids.MAGIC_POTION4,
        osrs.item_ids.MAGIC_POTION3,
        osrs.item_ids.MAGIC_POTION2,
        osrs.item_ids.MAGIC_POTION1,
    ],
    "SUPER_ANTI_POISION": [
        osrs.item_ids.SUPERANTIPOISON4,
        osrs.item_ids.SUPERANTIPOISON3,
        osrs.item_ids.SUPERANTIPOISON2,
        osrs.item_ids.SUPERANTIPOISON1,
        osrs.item_ids.ANTIPOISON1,
        osrs.item_ids.ANTIPOISON2,
        osrs.item_ids.ANTIPOISON3,
        osrs.item_ids.ANTIPOISON4,
        osrs.item_ids.ANTIDOTE1,
        osrs.item_ids.ANTIDOTE2,
        osrs.item_ids.ANTIDOTE3,
        osrs.item_ids.ANTIDOTE4,
        osrs.item_ids.ANTIDOTE1_5958,
        osrs.item_ids.ANTIDOTE2_5956,
        osrs.item_ids.ANTIDOTE3_5954,
        osrs.item_ids.ANTIDOTE4_5952,
    ],
    "ANTIFIRE": [
        osrs.item_ids.ANTIFIRE_POTION1,
        osrs.item_ids.ANTIFIRE_POTION2,
        osrs.item_ids.ANTIFIRE_POTION3,
        osrs.item_ids.ANTIFIRE_POTION4,
        osrs.item_ids.EXTENDED_ANTIFIRE4,
        osrs.item_ids.EXTENDED_ANTIFIRE3,
        osrs.item_ids.EXTENDED_ANTIFIRE2,
        osrs.item_ids.EXTENDED_ANTIFIRE1,
    ],
    'SUPER_ANTIFIRE': [
        osrs.item_ids.EXTENDED_SUPER_ANTIFIRE4,
        osrs.item_ids.EXTENDED_SUPER_ANTIFIRE3,
        osrs.item_ids.EXTENDED_SUPER_ANTIFIRE2,
        osrs.item_ids.EXTENDED_SUPER_ANTIFIRE1,
        osrs.item_ids.SUPER_ANTIFIRE_POTION1,
        osrs.item_ids.SUPER_ANTIFIRE_POTION2,
        osrs.item_ids.SUPER_ANTIFIRE_POTION3,
        osrs.item_ids.SUPER_ANTIFIRE_POTION4,
    ],
    "PRAYER": [
        osrs.item_ids.PRAYER_POTION4,
        osrs.item_ids.PRAYER_POTION3,
        osrs.item_ids.PRAYER_POTION2,
        osrs.item_ids.PRAYER_POTION1,
        osrs.item_ids.SUPER_RESTORE1,
        osrs.item_ids.SUPER_RESTORE2,
        osrs.item_ids.SUPER_RESTORE3,
        osrs.item_ids.SUPER_RESTORE4,
    ],
    "ANTIVENOM": [
        osrs.item_ids.EXTENDED_ANTIVENOM4,
        osrs.item_ids.EXTENDED_ANTIVENOM3,
        osrs.item_ids.EXTENDED_ANTIVENOM2,
        osrs.item_ids.EXTENDED_ANTIVENOM1,
        osrs.item_ids.ANTIVENOM4,
        osrs.item_ids.ANTIVENOM3,
        osrs.item_ids.ANTIVENOM2,
        osrs.item_ids.ANTIVENOM1,
        osrs.item_ids.ANTIVENOM4_12913,
        osrs.item_ids.ANTIVENOM3_12915,
        osrs.item_ids.ANTIVENOM2_12917,
        osrs.item_ids.ANTIVENOM1_12919,
    ]
}

prayer_map = {
    'protect_melee': 4118,
    'protect_range': 4117,
    'protect_mage': 4116,
    'rigour': 5464,
    'piety': 4129
}

prayer_map_widgets = {
    'protect_melee': '541,23',
    'protect_range': '541,22',
    'protect_mage': '541,21',
    'rigour': '541,33',
    'piety': '541,35'
}

# save values so i dont query over and over since this never really changes
prayer_widget_cache = {}
prayer_timeout = {}


def prayer_handler(qh: osrs.queryHelper.QueryHelper or None, prayers, cached_locations=False, ):
    curr_pos = pyautogui.position()
    if qh is None:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_skills({'prayer'})
        qh.set_widgets(pot_handler_required_prayer_widgets)
        qh.set_active_prayers()
        qh.query_backend()
    if not prayers:
        return
    if qh.get_skills('prayer') and qh.get_skills('prayer')['boostedLevel'] == 0:
        print('tried to turn on prayer but i have no prayer points!')
        return False
    moved = False
    for prayer in prayers:
        if prayer_map[prayer] not in qh.get_active_prayers():
            osrs.keeb.press_key('f5')
            start = datetime.now()
            if cached_locations and prayer_widget_cache and prayer_map_widgets[prayer] in prayer_widget_cache:
                if prayer in prayer_timeout and (datetime.now() - prayer_timeout[prayer]).total_seconds() < 0.6:
                    osrs.dev.logger.warning("Tried turning on the same prayer too quickly - blocking action.")
                    osrs.keeb.press_key('esc')
                    return
                osrs.move.fast_click_v2(prayer_widget_cache[prayer_map_widgets[prayer]])
                prayer_timeout[prayer] = datetime.now()
                osrs.dev.logger.info("Prayer switch wait time: %s", (datetime.now() - start).total_seconds())
                osrs.keeb.press_key('esc')
                return
            while True:
                qh.query_backend()
                if qh.get_widgets(prayer_map_widgets[prayer]):
                    prayer_widget_cache[prayer_map_widgets[prayer]] = qh.get_widgets(prayer_map_widgets[prayer])
                    if prayer in prayer_timeout and (datetime.now() - prayer_timeout[prayer]).total_seconds() < 0.6:
                        osrs.dev.logger.warning("Tried turning on the same prayer too quickly - blocking action.")
                        osrs.keeb.press_key('esc')
                        return
                    osrs.move.fast_click_v2(qh.get_widgets(prayer_map_widgets[prayer]))
                    prayer_timeout[prayer] = datetime.now()
                    moved = True
                    osrs.dev.logger.info("Prayer switch wait time: %s", (datetime.now() - start).total_seconds())
                    break
                elif (datetime.now() - start).total_seconds() > 1:
                    osrs.dev.logger.info("Time out waiting to prayer switch")
                    break
                else:
                    print('prayers not found')
    if moved:
        pyautogui.moveTo(curr_pos[0], curr_pos[1])
    osrs.keeb.press_key('esc')


def food_handler(qh, min_health):
    if not qh:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_inventory()
        qh.set_skills({'hitpoints'})
        qh.query_backend()
    if qh.get_skills('hitpoints')['boostedLevel'] < min_health:
        k = qh.get_inventory(food_ids)
        if not k:
            return False
        osrs.move.fast_click_v2(k)
        osrs.clock.sleep_one_tick()
    return True


def fast_food_handler(qh, min_health):
    if not qh:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_inventory()
        qh.set_skills({'hitpoints'})
        qh.query_backend()
    if qh.get_skills('hitpoints')['boostedLevel'] < min_health:
        k = qh.get_inventory(food_ids)
        if not k:
            return False
        osrs.move.fast_click_v2(k)
    return True


def pot_handler(qh: osrs.queryHelper.QueryHelper or None, pots, min_prayer=15, min_run=35):
    ANTIFIRE_VARBIT = '3981'
    SUPER_ANTIFIRE_VARBIT = '6101'
    if not qh:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
        qh.set_inventory()
        qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62', osrs.widget_ids.run_energy_widget_id})
        qh.set_varbit(ANTIFIRE_VARBIT if 'ANTIFIRE' in pots else SUPER_ANTIFIRE_VARBIT)
        qh.set_active_prayers()
        qh.query_backend()
    if 'SUPER_COMBATS' in pots \
            and pots['SUPER_COMBATS'] \
            and qh.get_skills('strength')['boostedLevel'] - qh.get_skills('strength')['level'] < 12:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_COMBATS'])
        if p:
            osrs.move.fast_click_v2(p)

    if 'SUPER_ATTACK' in pots \
            and pots['SUPER_ATTACK'] \
            and qh.get_skills('attack')['boostedLevel'] - qh.get_skills('attack')['level'] < 12:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_ATTACK'])
        if p:
            osrs.move.fast_click_v2(p)

    if 'SUPER_STRENGTH' in pots \
            and pots['SUPER_STRENGTH'] \
            and qh.get_skills('strength')['boostedLevel'] - qh.get_skills('strength')['level'] < 12:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_STRENGTH'])
        if p:
            osrs.move.fast_click_v2(p)

    if 'SUPER_DEFENCE' in pots \
            and pots['SUPER_DEFENCE'] \
            and qh.get_skills('defence')['boostedLevel'] - qh.get_skills('defence')['level'] < 12:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_DEFENCE'])
        if p:
            osrs.move.fast_click_v2(p)

    if 'RANGING_POTION' in pots \
            and pots['RANGING_POTION'] \
            and qh.get_skills('ranged')['boostedLevel'] - qh.get_skills('ranged')['level'] < 7:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['RANGING_POTION'])
        if p:
            osrs.move.fast_click_v2(p)

    if 'MAGIC_POTION' in pots \
            and pots['MAGIC_POTION'] \
            and qh.get_skills('magic')['boostedLevel'] - qh.get_skills('magic')['level'] < 3:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['MAGIC_POTION'])
        if p:
            osrs.move.fast_click_v2(p)

    if 'SUPER_ANTI_POISION' in pots \
            and pots['SUPER_ANTI_POISION'] \
            and int(qh.get_var_player('102')) > 0:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_ANTI_POISION'])
        if p:
            osrs.move.fast_click_v2(p)
        else:
            return False
    if 'ANTIVENOM' in pots \
            and pots['ANTIVENOM'] \
            and int(qh.get_var_player('102')) > 0:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['ANTIVENOM'])
        if p:
            osrs.move.fast_click_v2(p)
        else:
            return False
    if 'ANTIFIRE' in pots \
            and pots['ANTIFIRE'] \
            and qh.get_varbit() == 0:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['ANTIFIRE'])
        if p:
            osrs.move.fast_click_v2(p)
        else:
            return False
    if 'SUPER_ANTIFIRE' in pots \
            and pots['SUPER_ANTIFIRE'] \
            and qh.get_varbit() == 0:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['SUPER_ANTIFIRE'])
        if p:
            osrs.move.fast_click_v2(p)
        else:
            return False
    if 'PRAYER' in pots \
            and pots['PRAYER'] \
            and qh.get_skills('prayer')['boostedLevel'] < min_prayer:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['PRAYER'])
        if p:
            osrs.move.fast_click_v2(p)
        else:
            return False
    if 'STAMINA' in pots \
            and qh.get_widgets(osrs.widget_ids.run_energy_widget_id) \
            and int(qh.get_widgets(osrs.widget_ids.run_energy_widget_id)['text']) <= min_run:
        p = osrs.inv.are_items_in_inventory_v2(qh.get_inventory(), pot_matcher['STAMINA'])
        if p:
            osrs.move.fast_click_v2(p)
        else:
            return False
    return True


def turn_on_quick_prayers(qh):
    if not qh:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_widgets({'160,21'})
        qh.query_backend()
    if qh.get_widgets('160,21'):
        if qh.get_widgets('160,21')['spriteID'] == 1066:
            return
        else:
            osrs.move.fast_click_v2(qh.get_widgets('160,21'))


def turn_off_quick_prayers(qh):
    if not qh:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_widgets({'160,21'})
        qh.query_backend()
    if qh.get_widgets('160,21'):
        if qh.get_widgets('160,21')['spriteID'] == 1063:
            return
        else:
            osrs.move.fast_click_v2(qh.get_widgets('160,21'))
