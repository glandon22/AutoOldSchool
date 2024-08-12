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
    43701, 43702, 43703, 4304,
    # mind, chaos, death, blood, body, cosmic, nat, law
    43705, 43706, 43707, 43708, 43709, 43710, 43711, 43712
}

def game_active():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_widgets({game_active_widget})
    qh.query_backend()
    if qh.get_widgets(game_active_widget):
        return True
    else:
        return False


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
                and qh.get_inventory(osrs.item_ids.ItemIDs.GUARDIAN_FRAGMENTS.value)['quantity'] >= 240):
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
        return True


def craft_guardian_essence():
    osrs.move.go_to_loc(3612, 9488)
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

def crafted_inv():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    if not qh.get_inventory(osrs.item_ids.ItemIDs.GUARDIAN_ESSENCE.value):
        return True


def in_game_arena():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_player_world_location()
    qh.query_backend()
    if 3589 <= qh.get_player_world_location('x') <= 3640 and \
            9484 <= qh.get_player_world_location('y') <= 9519:
        return True


def craft_runes():
    crafting_info = determine_altar()
    osrs.move.interact_with_object(
        crafting_info['altar'], 'x', 1, False,
        custom_exit_function=crafted_inv
    )
    osrs.move.interact_with_object(
        crafting_info['exit'], 'x', 1, False,
        custom_exit_function=in_game_arena
    )


def rune_creation_handler():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_objects_v2('game', rifts)
    qh.set_player_world_location()
    while True:
        qh.query_backend()
        # i have entered a rift and am no longer in the GOTR lobby
        if (not (3586 <= qh.get_player_world_location('x') <= 3642)
                and not (9484 <= qh.get_player_world_location('y') <= 9520)):
            return craft_runes()
        if qh.get_objects_v2('game'):
            # combine all the different rifts into one list
            active_rifts = list(
                filter(lambda rift: rift['animation'] == 9363, qh.get_objects_v2('game'))
            )
            # I need to create a more intelligent rift selection method
            # isntead of just going to the closest one, but this will work
            # for initial QA of the logic
            closest = sorted(active_rifts, key=lambda obj: obj['dist'])
            if closest:
                osrs.move.fast_click(closest[0])


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


def charge_guardian():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs(['11403'])
    qh.set_inventory()
    while True:
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
        ]):
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

while True:
    main()
    while True:
        craft_guardian_essence()
        rune_creation_handler()
        charge_guardian()
        place_cell()
        osrs.move.interact_with_object(
            43696, 'x', 1, False,
            custom_exit_function=stored_runes, intermediate_tile='3609,9494,0'
        )
        if not game_active():
            break
