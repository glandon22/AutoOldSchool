import datetime

import osrs


'''
anim when rift active = 9363, inactive it is 9362
fire: 43704
nature: 43711
earth: 43703
water: 43702
cosmic: 43710
air: 43701
mind: 43705
body: 43709
chaos: 43706
death: 43707
law: 43712
blood: 43708

y >= 9483
'''

craftable_runes = [
    osrs.item_ids.ItemIDs.FIRE_RUNE.value,
    osrs.item_ids.ItemIDs.NATURE_RUNE.value,
    osrs.item_ids.ItemIDs.EARTH_RUNE.value,
    osrs.item_ids.ItemIDs.WATER_RUNE.value,
    osrs.item_ids.ItemIDs.COSMIC_RUNE.value,
    osrs.item_ids.ItemIDs.AIR_RUNE.value,
    osrs.item_ids.ItemIDs.MIND_RUNE.value,
    osrs.item_ids.ItemIDs.BODY_RUNE.value,
    osrs.item_ids.ItemIDs.CHAOS_RUNE.value,
    osrs.item_ids.ItemIDs.DEATH_RUNE.value,
    osrs.item_ids.ItemIDs.LAW_RUNE.value,
    osrs.item_ids.ItemIDs.BLOOD_RUNE.value,
]


# 9365 anim for making ess
uncharged_cell_id = 26882
game_active_widget = '746,23'
large_guardian_remains = 43719


rifts = {
    # air, water, earth, fire
    43701, 43702, 43703, 43704,
    # mind, chaos, death, blood, body, cosmic, nat, law
    43705, 43706, 43707, 43708, 43709, 43710, 43711, 43712
}

def repair_pouches():
    # have runes for spell s[rite-d =568
    main_chat_widget = '162,34'
    mage_widget = '75,14'
    spellbook_widget = '161,65'
    contact_widget = '218,108'
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({mage_widget, spellbook_widget, contact_widget, main_chat_widget})
    while True:
        qh.query_backend()
        if qh.get_widgets(mage_widget):
            osrs.move.click(qh.get_widgets(mage_widget))
            osrs.clock.random_sleep(3, 3.1)
            osrs.keeb.press_key('esc')
            break
        elif qh.get_widgets(spellbook_widget) and qh.get_widgets(spellbook_widget)['spriteID'] != 1027:
            osrs.keeb.press_key('f6')
        elif qh.get_widgets(contact_widget) \
                and not qh.get_widgets(contact_widget)['isHidden'] \
                and qh.get_widgets(contact_widget)['spriteID'] == 568:
            osrs.move.click(qh.get_widgets(contact_widget))
    osrs.player.dialogue_handler(["Can you repair my pouches?", "Thanks."])


def game_active():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({game_active_widget})
    qh.query_backend()
    if qh.get_widgets(game_active_widget):
        return True
    else:
        return False


def enter_game():
    print('entering the game arena')
    entry_gate = 43700
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_objects_v2('game', {entry_gate})
    gate_click = datetime.datetime.now() - datetime.timedelta(hours=2)
    while True:
        qh.query_backend()
        if qh.get_player_world_location('y') >= 9484:
            return
        elif qh.get_objects_v2('game', entry_gate) and (datetime.datetime.now() - gate_click).total_seconds() > 4:
            osrs.move.fast_click(qh.get_objects_v2('game', entry_gate)[0])
            gate_click = datetime.datetime.now()
        else:
            osrs.keeb.press_key('f1')
            osrs.keeb.press_key('esc')

def parse_guardian_power_level():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({'746,18'})
    qh.query_backend()
    raw = qh.get_widgets('746,18')
    if not raw:
        return 0
    return int(raw['text'].split(': ')[1][:-1])



def get_cells():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if qh.get_inventory(uncharged_cell_id) and qh.get_inventory(uncharged_cell_id)['quantity'] >= 10:
        return True


def mine_guardian_fragments():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({game_active_widget})
    qh.set_inventory()
    qh.set_is_mining()
    qh.set_objects_v2('game', {large_guardian_remains})
    while True:
        qh.query_backend()
        if (qh.get_inventory(osrs.item_ids.ItemIDs.GUARDIAN_FRAGMENTS.value)
                and qh.get_inventory(osrs.item_ids.ItemIDs.GUARDIAN_FRAGMENTS.value)['quantity'] >= 300):
            return
        elif (qh.get_widgets(game_active_widget)
              and not qh.get_is_mining()
              and qh.get_objects_v2('game', large_guardian_remains)):
            osrs.move.fast_click(qh.get_objects_v2('game', large_guardian_remains)[0])


def completed_essence_crafting():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.GUARDIAN_FRAGMENTS.value):
        return True
    elif len(qh.get_inventory()) >= 28:
        if qh.get_inventory(osrs.item_ids.ItemIDs.COLOSSAL_POUCH.value):
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.COLOSSAL_POUCH.value))
            osrs.clock.random_sleep(1, 1.01)
        return True


def craft_guardian_essence():
    osrs.move.go_to_loc(3612, 9488)
    # fill the colossal pouch
    osrs.move.interact_with_object(
        43754, 'x', 3636, False,
        custom_exit_function=completed_essence_crafting
    )
    osrs.move.interact_with_object(
        43754, 'x', 3636, False,
        custom_exit_function=completed_essence_crafting
    )
    osrs.move.interact_with_object(
        43754, 'x', 3636, False,
        custom_exit_function=completed_essence_crafting
    )

'''
death 34770 exit -> 34758
laws 34767 34755
'''
def determine_altar():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        # air
        if 2835 <= qh.get_player_world_location('x') <= 2851:
            return {'altar': 34760, 'exit': 34748}
        # water
        elif 2707 <= qh.get_player_world_location('x') <= 2732:
            return {'altar': 34762, 'exit': 34750}
        # earth
        elif 2628 <= qh.get_player_world_location('x') <= 2680:
            return {'altar': 34763, 'exit': 34751}
        # fire
        elif 2560 <= qh.get_player_world_location('x') <= 2605:
            return {'altar': 34764, 'exit': 34752}
        # mind
        elif 2761 <= qh.get_player_world_location('x') <= 2802:
            return {'altar': 34761, 'exit': 34749}
        # body
        elif 2506 <= qh.get_player_world_location('x') <= 2538:
            return {'altar': 34765, 'exit': 34753}
        # nats
        elif 2390 <= qh.get_player_world_location('x') <= 2409:
            return {'altar': 34768, 'exit': 34756}
        # law
        elif 2444 <= qh.get_player_world_location('x') <= 2484:
            return {'altar': 34767, 'exit': 34755}
        # death
        elif 2191 <= qh.get_player_world_location('x') <= 2221:
            return {'altar': 34770, 'exit': 34758}
        # chaos
        elif 2244 <= qh.get_player_world_location('x') <= 2298:
            return {'altar': 34769, 'exit': 34757}
        # cosmic
        elif 2118 <= qh.get_player_world_location('x') <= 2166:
            return {'altar': 34766, 'exit': 34754}


def crafted_inv():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_canvas()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.GUARDIAN_ESSENCE.value):
        if qh.get_inventory(osrs.item_ids.ItemIDs.COLOSSAL_POUCH.value):
            osrs.move.right_click_v6(
                qh.get_inventory(osrs.item_ids.ItemIDs.COLOSSAL_POUCH.value),
                'Empty',
                qh.get_canvas(),
                in_inv=True
            )
            osrs.clock.random_sleep(1, 1.01)
        return True


def in_game_arena():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 3589 <= qh.get_player_world_location('x') <= 3640 and \
            9484 <= qh.get_player_world_location('y') <= 9519:
        return True


def find_cosmic_altar():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {34766})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_objects_v2('game', 34766):
            print('here')
            return
        elif 2140 <= qh.get_player_world_location('x') <= 2144 and 4852 <= qh.get_player_world_location('y') <= 4856:
            osrs.move.run_towards_square_v2({'x': 2142, 'y': 4837, 'z': 0})


def find_fire_altar():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', {34764})
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        if qh.get_objects_v2('game', 34764) and qh.get_player_world_location('x') >= 2579:
            print('here')
            return
        else:
            osrs.move.go_to_loc(2581, 4841)


# mind altar and law altar exits are not visible from crafting loc
def go_to_altar_exits():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.set_tiles({
        '2464,4823,0',
        '2790,4832,0'
    })
    altar_info = determine_altar()
    qh.query_backend()
    # mind
    if altar_info['altar'] == 34761 and qh.get_player_world_location('y') >= 4833 and qh.get_tiles('2790,4832,0'):
        osrs.move.fast_click(qh.get_tiles('2790,4832,0'))

    # law
    elif altar_info['altar'] == 34767 and qh.get_player_world_location('y') >= 4824 and qh.get_tiles('2464,4823,0'):
        osrs.move.fast_click(qh.get_tiles('2464,4823,0'))


def craft_runes():
    # if you spawn in to the north side of the cosmic altar you cant see the actual altar
    crafting_info = determine_altar()
    if crafting_info['altar'] == 34766:
        find_cosmic_altar()
    elif crafting_info['altar'] == 34764:
        find_fire_altar()

    # empty ess pouch

    osrs.move.interact_with_object(
        crafting_info['altar'], 'x', 1, False,
        custom_exit_function=crafted_inv, obj_dist=20
    )
    osrs.move.interact_with_object(
        crafting_info['altar'], 'x', 1, False,
        custom_exit_function=crafted_inv, obj_dist=20
    )
    osrs.move.interact_with_object(
        crafting_info['altar'], 'x', 1, False,
        custom_exit_function=crafted_inv, obj_dist=20
    )
    osrs.move.interact_with_object(
        crafting_info['exit'], 'x', 1, False,
        custom_exit_function=in_game_arena, obj_dist=23, pre_interact=go_to_altar_exits
    )


def find_altar(active_rifts):
    altar_preferences = [
        # 43708, blood
        43707,  # death
        43704,  # fire
        43712,  # law
        43711,  # nat
        #43703,  # earth
        #43702,  # water
        43710,  # cosmic
        43706,  # chaos
        #43701,  # air
        #43705,  # mind
        43709,  # body
    ]
    for altar in altar_preferences:
        for rift in active_rifts:
            if rift['id'] == altar:
                return rift


def rune_creation_handler():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', rifts)
    qh.set_player_world_location()
    game_last_active = datetime.datetime.now()
    while True:
        qh.query_backend()

        # if the game ends while i am searching for a portal to enter it will stall
        if not game_active() and (datetime.datetime.now() - game_last_active).total_seconds() > 5:
            return
        elif game_active():
            game_last_active = datetime.datetime.now()

        # i have entered a rift and am no longer in the GOTR lobby
        if (not (3586 <= qh.get_player_world_location('x') <= 3642)
                and not (9484 <= qh.get_player_world_location('y') <= 9520)):
            return craft_runes()
        if qh.get_objects_v2('game'):
            # combine all the different rifts into one list
            active_rifts = list(
                filter(lambda rift: rift['animation'] == 9363, qh.get_objects_v2('game'))
            )
            rift = find_altar(active_rifts)
            if rift:
                osrs.move.fast_click(rift)


def main():
    osrs.move.interact_with_object(
        43732, 'x', 1, False,
        custom_exit_function=get_cells, right_click_option='Take-10', timeout=10
    )
    osrs.move.go_to_loc(3633, 9502)
    osrs.move.interact_with_object(
        43724, 'x', 3634, True, obj_type='ground'
    )
    mine_guardian_fragments()
    osrs.move.interact_with_object(
        43726, 'x', 3636, False, obj_type='ground'
    )
    osrs.move.go_to_loc(3623, 9495)


def charge_guardian():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['11403'])
    qh.set_inventory()
    game_last_active = datetime.datetime.now()
    while True:
        if not game_active() and (datetime.datetime.now() - game_last_active).total_seconds() > 5:
            return
        elif game_active():
            game_last_active = datetime.datetime.now()
        qh.query_backend()

        if not qh.get_inventory([
            osrs.item_ids.ItemIDs.CATALYTIC_GUARDIAN_STONE.value,
            osrs.item_ids.ItemIDs.ELEMENTAL_GUARDIAN_STONE.value,
        ]):
            return
        elif qh.get_npcs():
            osrs.move.fast_click(qh.get_npcs()[0])


def place_cell():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('ground', {43740, 43741, 43741, 43742, 43743})
    qh.set_inventory()
    while True:
        qh.query_backend()
        if not qh.get_inventory([
            osrs.item_ids.ItemIDs.OVERCHARGED_CELL.value,
            osrs.item_ids.ItemIDs.MEDIUM_CELL.value,
            osrs.item_ids.ItemIDs.STRONG_CELL.value,
            osrs.item_ids.ItemIDs.WEAK_CELL.value,
        ]) or not game_active():
            return
        elif qh.get_objects_v2('ground'):
            closest = sorted(qh.get_objects_v2('ground'), key=lambda obj: obj['dist'])
            if closest:
                osrs.move.fast_click(closest[0])


def stored_runes():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(craftable_runes):
        return True


def get_points():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        craft_guardian_essence()
        osrs.move.go_to_loc(3614, 9494)
        rune_creation_handler()
        charge_guardian()
        place_cell()
        osrs.move.interact_with_object(
            43696, 'x', 1, False,
            custom_exit_function=stored_runes, intermediate_tile='3609,9494,0'
        )
        guardian_power = parse_guardian_power_level()
        qh.query_backend()
        print('gp',guardian_power)
        if guardian_power > 88 or not qh.get_inventory(osrs.item_ids.ItemIDs.GUARDIAN_FRAGMENTS.value):
            while True:
                if not game_active():
                    return
enter_game()
while True:
    osrs.game.break_manager_v4({
        'intensity': 'low',
        'logout': False,
        'login': enter_game
    })
    main()
    get_points()
    repair_pouches()
