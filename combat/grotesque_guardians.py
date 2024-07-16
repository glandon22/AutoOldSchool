'''
notes

turn on pray range
click bell - 31669
attack dawn and pray range
once at 55% dawn will go away
equie melee gear and pray melee w piety or whatever
attack dusk until u see projectile 1435, then run away!
one projectile 1435 is gone attack him again
during fight proj 1435 will occasionally appear and need to be dodged. think i can move two steps right and should be fine
when dawn is back that means next phase
during this interlude there are lava pools on ground but idk ids yet
then dawn will throw out the 3 balls i need to pick up id 31688, 31687,31686
attack dawn until she disappears
dawn will disappear then the fire prison spec happens. need to run away during that
after game obj id 26209


during all dawn phases she shoots out proj 1445 which needs to be avoided by moving squares

dawn 7852, 7884

dusk 7882, 7888

1416 - 1424 magma tiles and they are graphics objects
1434 - graphics objects - firewall prison spec need to run 3 squares from my curr loc


first chain up - 16537 3422,3550,0 to z == 1
stairs up - 2119 3414,3540,1 z == 2
stairs to grot - 31681 3428,3543,2
'''
import datetime

import osrs
from osrs.item_ids import ItemIDs

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
    ],
    "SUPER_RESTORE": [
        ItemIDs.SUPER_RESTORE4.value,
        ItemIDs.SUPER_RESTORE3.value,
        ItemIDs.SUPER_RESTORE2.value,
        ItemIDs.SUPER_RESTORE1.value,
    ]
}

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


def start_fight():
    corner_anchor_spot = '31644'
    start_bell_id = '31669'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['dawn'])
    qh.set_player_world_location()
    qh.set_active_prayers()
    qh.set_inventory()
    qh.set_skills({'ranged'})
    qh.set_widgets({prayer_map_widgets['protect_range']})
    anchor_tile = None
    last_prayer_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_pot_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    osrs.keeb.press_key('f5')
    osrs.keeb.press_key('esc')
    while True:
        qh.query_backend()
        nearby_tiles = osrs.util.generate_surrounding_tiles_from_point(30, qh.get_player_world_location())
        qh.set_objects(
            set(nearby_tiles),
            {start_bell_id, corner_anchor_spot},
            osrs.queryHelper.ObjectTypes.GAME.value
        )
        if qh.get_npcs_by_name():
            break
        elif prayer_map['protect_range'] not in qh.get_active_prayers() \
                and qh.get_widgets(prayer_map_widgets['protect_range']) \
                and (datetime.datetime.now() - last_prayer_click).total_seconds() > 1.2:
            osrs.keeb.press_key('f5')
            osrs.move.fast_click(qh.get_widgets(prayer_map_widgets['protect_range']))
            osrs.keeb.press_key('esc')
            last_prayer_click = datetime.datetime.now()
        elif qh.get_skills('ranged') \
                and qh.get_skills('ranged')['boostedLevel'] <= qh.get_skills('ranged')['level'] \
                and qh.get_inventory(pot_matcher['RANGING_POTION']) \
                and (datetime.datetime.now() - last_pot_click).total_seconds() > 1.2:
            osrs.move.fast_click(qh.get_inventory(pot_matcher['RANGING_POTION']))
        elif qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, start_bell_id):
            bell = qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, start_bell_id)[0]
            osrs.move.fast_click(bell)
            if not anchor_tile and qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, corner_anchor_spot):
                corners = qh.get_objects(osrs.queryHelper.ObjectTypes.GAME.value, corner_anchor_spot)
                for corner in corners:
                    if corner['x_coord'] > bell['x_coord']:
                        anchor_tile = {'x': corner['x_coord'], 'y': corner['y_coord']}

    return anchor_tile

'''
    dusk_immune_id = '7851'
    dusk_id = '7882'
    dusk_end_id = '7855'
    dawn_end_id = '7853'
'''

# Need to figure out how to ensure i dodge the stone attack from dawn here
# and how to trap dusk in that corner
def phase_1_dawn(anchor):
    dawn_id = '7852'
    lure_start_tile = f'{anchor["x"] + 5},{anchor["y"] - 4},0'
    lure_end_tile = f'{anchor["x"] + 2},{anchor["y"] - 4},0'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs([dawn_id])
    qh.set_projectiles()
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_skills({'hitpoints', 'prayer'})
    qh.set_tiles({lure_start_tile, lure_end_tile})
    qh.set_interating_with()
    qh.set_active_prayers()
    qh.set_widgets({prayer_map_widgets['protect_range'], prayer_map_widgets['rigour']})
    last_rigour_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_prot_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    seen_dawn = False
    while True:
        qh.query_backend()
        if len(qh.get_npcs()) > 0 and not seen_dawn:
            print('npcs: ', qh.get_npcs())
            seen_dawn = True
        if len(qh.get_npcs()) == 0 and seen_dawn:
            return
        elif qh.get_skills('hitpoints')['boostedLevel'] < 35:
            if qh.get_inventory(ItemIDs.ANGLERFISH.value):
                osrs.move.fast_click(ItemIDs.ANGLERFISH.value)
            else:
                return osrs.game.tele_home()
        elif qh.get_skills('prayer')['boostedLevel'] < 20:
            if qh.get_inventory(pot_matcher['SUPER_RESTORE']):
                osrs.move.fast_click(qh.get_inventory(pot_matcher['SUPER_RESTORE']))
            elif qh.get_inventory(pot_matcher['PRAYER']):
                osrs.move.fast_click(qh.get_inventory(pot_matcher['PRAYER']))
            else:
                return osrs.game.tele_home()
        elif not qh.get_interating_with() and qh.get_npcs():
            osrs.move.fast_click(qh.get_npcs()[0])
        elif prayer_map['rigour'] not in qh.get_active_prayers() and qh.get_widgets(prayer_map_widgets['rigour']) \
                and (datetime.datetime.now() - last_rigour_click).total_seconds() > 1.2:
            osrs.keeb.press_key('f5')
            osrs.move.fast_click(qh.get_widgets(prayer_map_widgets['rigour']))
            osrs.keeb.press_key('esc')
            last_rigour_click = datetime.datetime.now()
        elif prayer_map['protect_range'] not in qh.get_active_prayers() \
                and qh.get_widgets(prayer_map_widgets['protect_range']) \
                and (datetime.datetime.now() - last_prot_click).total_seconds() > 1.2:
            osrs.keeb.press_key('f5')
            osrs.move.fast_click(qh.get_widgets(prayer_map_widgets['protect_range']))
            osrs.keeb.press_key('esc')
            last_prot_click = datetime.datetime.now()


'''
x + 5, y - 4 to start
x + 2, y - 4 to to trap
'''