import osrs


pot_handler_required_prayer_widgets = {'233,0', '541,23', '541,22', '541,21', '161,62', '541,25'}
pot_handler_required_skills = {'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'}
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

pot_matcher = {
    "SUPER_COMBATS": [
        osrs.item_ids.ItemIDs.SUPER_COMBAT_POTION4.value,
        osrs.item_ids.ItemIDs.SUPER_COMBAT_POTION3.value,
        osrs.item_ids.ItemIDs.SUPER_COMBAT_POTION2.value,
        osrs.item_ids.ItemIDs.SUPER_COMBAT_POTION1.value
    ],
    "SUPER_ATTACK": [
        osrs.item_ids.ItemIDs.SUPER_ATTACK4.value,
        osrs.item_ids.ItemIDs.SUPER_ATTACK3.value,
        osrs.item_ids.ItemIDs.SUPER_ATTACK2.value,
        osrs.item_ids.ItemIDs.SUPER_ATTACK1.value,
    ],
    "SUPER_STRENGTH": [
        osrs.item_ids.ItemIDs.SUPER_STRENGTH4.value,
        osrs.item_ids.ItemIDs.SUPER_STRENGTH3.value,
        osrs.item_ids.ItemIDs.SUPER_STRENGTH2.value,
        osrs.item_ids.ItemIDs.SUPER_STRENGTH1.value,
    ],
    "SUPER_DEFENCE": [
        osrs.item_ids.ItemIDs.SUPER_DEFENCE4.value,
        osrs.item_ids.ItemIDs.SUPER_DEFENCE3.value,
        osrs.item_ids.ItemIDs.SUPER_DEFENCE2.value,
        osrs.item_ids.ItemIDs.SUPER_DEFENCE1.value,
    ],
    "RANGING_POTION": [
        osrs.item_ids.ItemIDs.RANGING_POTION4.value,
        osrs.item_ids.ItemIDs.RANGING_POTION3.value,
        osrs.item_ids.ItemIDs.RANGING_POTION2.value,
        osrs.item_ids.ItemIDs.RANGING_POTION1.value,
    ],
    "MAGIC_POTION": [
        osrs.item_ids.ItemIDs.MAGIC_POTION4.value,
        osrs.item_ids.ItemIDs.MAGIC_POTION3.value,
        osrs.item_ids.ItemIDs.MAGIC_POTION2.value,
        osrs.item_ids.ItemIDs.MAGIC_POTION1.value,
    ],
    "SUPER_ANTI_POISION": [
        osrs.item_ids.ItemIDs.SUPERANTIPOISON4.value,
        osrs.item_ids.ItemIDs.SUPERANTIPOISON3.value,
        osrs.item_ids.ItemIDs.SUPERANTIPOISON2.value,
        osrs.item_ids.ItemIDs.SUPERANTIPOISON1.value,
    ],
    "EXTENDED_ANTIFIRE": [
        osrs.item_ids.ItemIDs.EXTENDED_ANTIFIRE4.value,
        osrs.item_ids.ItemIDs.EXTENDED_ANTIFIRE3.value,
        osrs.item_ids.ItemIDs.EXTENDED_ANTIFIRE2.value,
        osrs.item_ids.ItemIDs.EXTENDED_ANTIFIRE1.value,
    ],
    "PRAYER": [
        osrs.item_ids.ItemIDs.PRAYER_POTION4.value,
        osrs.item_ids.ItemIDs.PRAYER_POTION3.value,
        osrs.item_ids.ItemIDs.PRAYER_POTION2.value,
        osrs.item_ids.ItemIDs.PRAYER_POTION1.value,
        osrs.item_ids.ItemIDs.SUPER_RESTORE1.value,
        osrs.item_ids.ItemIDs.SUPER_RESTORE2.value,
        osrs.item_ids.ItemIDs.SUPER_RESTORE3.value,
        osrs.item_ids.ItemIDs.SUPER_RESTORE4.value,
    ]
}

prayer_map = {
    'protect_melee': 4118,
    'protect_range': 4117,
    'protect_mage': 4116,
    'redemption': 4120
}

prayer_map_widgets = {
    'protect_melee': '541,23',
    'protect_range': '541,22',
    'protect_mage': '541,21',
    'redemption': '541,25'
}


def prayer_handler(qh: osrs.queryHelper.QueryHelper or None, prayers):
    # pre load the prayer widget locations
    osrs.keeb.press_key('f5')
    osrs.keeb.press_key('esc')
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
    for prayer in prayers:
        if prayer_map[prayer] not in qh.get_active_prayers():
            osrs.keeb.press_key('f5')
            qh.query_backend()
            if qh.get_widgets(prayer_map_widgets[prayer]):
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


def pot_handler(qh: osrs.queryHelper.QueryHelper or None, pots):
    ANTIFIRE_VARBIT = '3981'
    if not qh:
        qh = osrs.queryHelper.QueryHelper()
        qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
        qh.set_inventory()
        qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62'})
        qh.set_varbit(ANTIFIRE_VARBIT)
        qh.set_active_prayers()
        qh.query_backend()
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
