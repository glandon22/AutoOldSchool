'''
notes
drakans to ver sinhaza run north to 3728, 3304
game obj 32637 to z == 1
run to 3808,9746,1
nightmage asleep is 9460
9432 in pre-fight, 9425 attackable
anim id 8594 is melee attack
anim id 8595 is mage attack
anim id 8596 is range attack
game objects 37444 are the safe flowers in the quartiles attack
9467, 9466 are the husks to quickly kill
1767 graphics obj is the black hands
'''
from datetime import datetime

import pyautogui
from scipy.stats import semicircular

import osrs

disease_pots = [
    osrs.item_ids.RELICYMS_BALM1,
    osrs.item_ids.RELICYMS_BALM2,
    osrs.item_ids.RELICYMS_BALM3,
    osrs.item_ids.RELICYMS_BALM4,
    osrs.item_ids.SANFEW_SERUM1,
    osrs.item_ids.SANFEW_SERUM2,
    osrs.item_ids.SANFEW_SERUM3,
    osrs.item_ids.SANFEW_SERUM4,
]


def add_unsafe_claw_tiles(bad_tiles: set, claws):
    for claw in claws:
        if claw['animation'] <= 50:
            bad_tiles.add(f"{claw['x_coord']},{claw['y_coord']}")
    return bad_tiles


def add_unsafe_spore_tiles(bad_tiles: set, spores):
    for spore in spores:
        # you cant get within one tile of these
        tiles = osrs.util.determine_large_monster_area({
            'x_coord': spore['x_coord'] - 1,
            'y_coord': spore['y_coord'] - 1,
        }, 3)
        for tile in tiles:
            bad_tiles.add(f"{tile['x']},{tile['y']}")
    return bad_tiles


def add_phosanis_tiles(bad_tiles: set, pnm):
    if not pnm:
        return bad_tiles
    pnm_area = osrs.util.determine_large_monster_area(pnm, 5)
    for tile in pnm_area:
        bad_tiles.add(f"{tile['x']},{tile['y']}")
    return bad_tiles


def add_pillar_tiles(bad_tiles: set, pillars):
    for pillar in pillars:
        pillar_area = osrs.util.determine_large_monster_area(pillar, 3)
        for tile in pillar_area:
            bad_tiles.add(f"{tile['x']},{tile['y']}")
    return bad_tiles


def go_to_nightmare():
    osrs.move.go_to_loc(3728, 3304)
    osrs.move.interact_with_object_v3(
        32637,
        coord_type='z',
        coord_value=1,
        greater_than=True
    )
    osrs.move.go_to_loc(3808, 9779, 1)
    osrs.move.interact_with_object_v3(
        29710,
        coord_type='z',
        coord_value=3
    )


def husk_handler(qh):
    npcs = qh.get_npcs()
    if not npcs:
        return

    husk1 = list(filter(
        lambda npc: npc['health'] != 0 and npc['id'] == 9466,
        npcs
    ))
    husk2 = list(filter(
        lambda npc: npc['health'] != 0 and npc['id'] == 9467,
        npcs
    ))

    # Attack husks if they are out
    if husk1:
        osrs.player.equip_item_no_wait([osrs.item_ids.ZOMBIE_AXE], qh.get_equipment())
        osrs.move.conditional_click(
            qh,
            husk1[0],
            'Attack'
        )
        return True
    elif husk2:
        osrs.player.equip_item_no_wait([osrs.item_ids.ZOMBIE_AXE], qh.get_equipment())
        osrs.move.conditional_click(
            qh,
            husk2[0],
            'Attack'
        )
        return True


def parasite_handler(qh: osrs.queryHelper.QueryHelper, interacting, claws):
    if claws:
        return osrs.dev.logger.warning("Parasite is out but claws are preventing me from attacking.")
    npcs = qh.get_npcs()
    if not npcs:
        return
    parasite = list(filter(
        lambda npc: npc['health'] != 0 and npc['id'] == 9469,
        npcs
    ))

    # Attack parasite if out
    if parasite:
        osrs.player.equip_item_no_wait([osrs.item_ids.ZOMBIE_AXE], qh.get_equipment())
        if not interacting or 'Parasite' not in interacting:
            osrs.move.conditional_click(
                qh,
                parasite[0],
                'Attack'
            )
        return True


def determine_safe_wave_dash_tiles(initial_pnm, anchor):
    osrs.dev.logger.info("calcing: %s", initial_pnm['orientation'])
    bad_tiles = {}
    for x in range(initial_pnm['x_coord'] - 2, initial_pnm['x_coord'] + 7):
        for y in range(anchor['y'] - 50, anchor['y'] + 50):
            bad_tiles[f'{x},{y},{3}'] = {'x': x, 'y': y, 'z': 3}
    for x in range(anchor['x'] - 50, anchor['x'] + 50):
        for y in range(initial_pnm['y_coord'] - 2, initial_pnm['y_coord'] + 7):
            bad_tiles[f'{x},{y},{3}'] = {'x': x, 'y': y, 'z': 3}
    total_area = osrs.util.generate_surrounding_tiles_from_point(
        12, {'x': initial_pnm['x_coord'], 'y': initial_pnm['y_coord'], 'z': 3}
    )
    safe_tiles = set()
    for tile in total_area:
        if tile not in bad_tiles:
            safe_tiles.add(tile)
    return safe_tiles


def wave_dash_handler(initial_pnm, anchor, main_qh):
    osrs.dev.logger.info("Handling Phosani's wave dash.")
    seen_dash = False
    safe_tiles = determine_safe_wave_dash_tiles(initial_pnm, anchor)
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(["Phosani's Nightmare", "Husk"])
    qh.set_player_world_location()
    qh.set_objects_v2('game', {37743, 37744, 37745})
    qh.set_tiles(safe_tiles)
    qh.set_interating_with()
    qh.set_active_prayers()
    while True:
        qh.query_backend()
        # no need to user overheads during this phase
        if qh.get_active_prayers():
            osrs.player.flick_all_prayers()
        pnm = osrs.util.find_closest_target_in_game(
            qh.get_npcs(),
            qh.get_player_world_location(),
            lambda npc: npc['name'] == "Phosani's Nightmare"
        )
        if pnm:
            osrs.dev.logger.debug(
                "pnm data: %s, %s, %s, %s",
                initial_pnm['x_coord'], pnm['x_coord'], initial_pnm['y_coord'], pnm['y_coord']
            )
        if pnm and pnm['animation'] == -1 and seen_dash:
            osrs.dev.logger.info("Successfully handle wave dash.")
            return True
        elif pnm and initial_pnm['x_coord'] != pnm['x_coord'] or initial_pnm['y_coord'] != pnm['y_coord']:
            osrs.dev.logger.info("Phosani has moved - exiting function")
            return True
        elif pnm and pnm['animation'] == 8597 and not seen_dash:
            osrs.dev.logger.info("Phosani has begun wave dash.")
            seen_dash = True

        # Ensure I am in a safe area and click away from pn so i dont follow her
        if (
                (f"{qh.get_player_world_location('x')},{qh.get_player_world_location('y')},3" not in safe_tiles
                 or (qh.get_interating_with() and not main_qh.get_widgets('413,1')))
                and qh.get_tiles()
        ):
            osrs.dev.logger.warning("I am in Phosani's wave dash path!")
            nearby_tiles = osrs.util.combine_objects(qh.get_tiles())
            nearest_safe_tile = sorted(nearby_tiles, key=lambda tile: tile['dist'])
            if nearest_safe_tile:
                osrs.dev.logger.info("Going to a safe tile to avoid wave dash.")
                osrs.move.fast_click_v2(nearest_safe_tile[0])
        else:
            osrs.dev.logger.info("I am on a safe tile - waiting for wave dash to end.")
            osrs.dev.logger.info('player: %s',
                                 f"{qh.get_player_world_location('x')},{qh.get_player_world_location('y')},3")
            osrs.dev.logger.info('safe_tiles: %s', safe_tiles)


def find_safe_quadrant(objects, anchor, tiles):
    n = list(filter(
        lambda obj: obj['x_coord'] == anchor['x'] and obj['y_coord'] == anchor['y'] + 1,
        objects
    ))
    e = list(filter(
        lambda obj: obj['x_coord'] == anchor['x'] + 1 and obj['y_coord'] == anchor['y'],
        objects
    ))
    s = list(filter(
        lambda obj: obj['x_coord'] == anchor['x'] and obj['y_coord'] == anchor['y'] - 1,
        objects
    ))
    w = list(filter(
        lambda obj: obj['x_coord'] == anchor['x'] - 1 and obj['y_coord'] == anchor['y'],
        objects
    ))

    # quadrant 1 is safe
    if n and e:
        #osrs.dev.logger.info("The northeast quadrant is safe for the flower attack.")
        return [tile for tile in tiles if tile['x_coord'] >= anchor['x'] and tile['y_coord'] >= anchor['y']]
    # quadrant 2 is safe
    elif s and e:
        #osrs.dev.logger.info("The southeast quadrant is safe for the flower attack.")
        return [tile for tile in tiles if tile['x_coord'] >= anchor['x'] and tile['y_coord'] <= anchor['y']]
    # quadrant 3 is safe
    elif s and w:
        #osrs.dev.logger.info("The southwest quadrant is safe for the flower attack.")
        return [tile for tile in tiles if tile['x_coord'] <= anchor['x'] and tile['y_coord'] <= anchor['y']]
    # quadrant 4 is safe
    elif n and w:
        #osrs.dev.logger.info("The northwest quadrant is safe for the flower attack.")
        return [tile for tile in tiles if tile['x_coord'] <= anchor['x'] and tile['y_coord'] >= anchor['y']]
    else:
        return tiles


def sleepwalker_handler():
    osrs.dev.logger.info("Sleepwalkers present - killing them all")
    qh = osrs.queryHelper.QueryHelper()
    qh.set_npcs_by_name(['Sleepwalker'])
    qh.set_right_click_menu()
    qh.set_player_world_location()
    qh.set_detailed_interating_with()
    while True:
        qh.query_backend()
        closest = osrs.util.find_closest_target_in_game(qh.get_npcs(), qh.get_player_world_location(),
                                                        lambda npc: npc['health'] != 0)
        if not closest:
            osrs.dev.logger.info("All sleepwalkers are down.")
            return
        elif (qh.get_detailed_interating_with()
              and qh.get_detailed_interating_with()['health'] != 0
              and 'Sleepwalker' in qh.get_detailed_interating_with()['name']):
            osrs.dev.logger.info("In combat with sleepwalker.")
            continue
        elif (qh.get_right_click_menu()
              and qh.get_right_click_menu()['entries']
              and qh.get_right_click_menu()['entries'][-1][0] == 'Attack'
              and 'Sleepwalker' in qh.get_right_click_menu()['entries'][-1][2]):
            pyautogui.click()
            osrs.dev.logger.info("Clicking a sleepwalker.")
        elif closest:
            osrs.move.instant_move(closest)
            osrs.dev.logger.info("Targeting a sleepwalker.")


def npc_parser(qh):
    pnm = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['name'] == "Phosani's Nightmare"
    )
    nw_totem = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] in [9441, 9440]
    )
    se_totem = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] in [9438, 9437]
    )
    sw_totem = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] in [9435, 9434]
    )
    ne_totem = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] in [9444, 9443]
    )
    nw_totem_charged = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] in [9442]
    )
    se_totem_charged = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] in [9439]
    )
    sw_totem_charged = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] in [9436]
    )
    ne_totem_charged = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] in [9445]
    )
    sleepwalker = osrs.util.find_closest_target_in_game(
        qh.get_npcs(),
        qh.get_player_world_location(),
        lambda npc: npc['id'] == 9470 and 'health' in npc and npc['health'] != 0
    )
    return [pnm, nw_totem, se_totem, sw_totem, ne_totem, nw_totem_charged, se_totem_charged, sw_totem_charged,
            ne_totem_charged, sleepwalker]


def curse_handler(qh):
    for i in range(0, 50):
        widget = f"162,56,{i * 4}"
        # this chat line is not populated
        if not qh.get_widgets(widget):
            continue

        if (qh.get_widgets(widget)
                and ('The Nightmare has awoken' in qh.get_widgets(widget)['text'] or 'curse wear off' in qh.get_widgets(widget)['text'])):
            return False
        if qh.get_widgets(widget) and 'has cursed you' in qh.get_widgets(widget)['text']:
            return True
    osrs.dev.logger.warning("No curse status found in chat box - defaulting to not cursed. Is the chat box closed?")
    return False


def determine_pillar_to_attack(qh, nw_totem, ne_totem, se_totem, sw_totem, any_spore):
    # NW totem is still alive
    if nw_totem:
        return nw_totem
    # NE totem is still alive
    elif ne_totem:
        return ne_totem
    # SE Totem is still up
    elif qh.get_widgets('413,27') and qh.get_widgets('413,27')['xMax'] - qh.get_widgets('413,27')[
        'xMin'] < 60:
        # dont attack totems if they are out of range during spore phase
        if se_totem:
            return se_totem
        # If I am too far north I will be unable to see these pillars, so run south
        elif qh.get_tiles(f"{qh.get_player_world_location('x')},{qh.get_player_world_location('y') - 3},3"):
            return {'x_coord': qh.get_player_world_location('x'), 'y_coord': qh.get_player_world_location('y') - 3}
    # SW Totem is still up
    elif (qh.get_widgets('413,21')
          and qh.get_widgets('413,21')['xMax'] - qh.get_widgets('413,21')['xMin'] < 60):
        osrs.player.equip_item_no_wait([osrs.item_ids.TRIDENT_OF_THE_SWAMP], qh.get_equipment())
        # dont attack totems if they are out of range during spore phase
        if sw_totem:
            return sw_totem
        # If I am too far north I will be unable to see these pillars, so run south
        elif qh.get_tiles(f"{qh.get_player_world_location('x')},{qh.get_player_world_location('y') - 3},3"):
            return {'x_coord': qh.get_player_world_location('x'), 'y_coord': qh.get_player_world_location('y') - 3}


def main():
    qh = osrs.queryHelper.QueryHelper()
    chat_lines = set()
    for i in range(0, 50):
        chat_lines.add(f"162,56,{i * 4}")
    qh.set_widgets(chat_lines)
    qh.set_widgets({'162,56,0'})
    # leaving this empty matches all npcs which i can filter later
    qh.set_npcs_by_name([])
    qh.set_objects_v2('graphics', {1767}, dist=8)
    qh.set_objects_v2('game', {37738, 37739, 37743, 37744, 37745})
    qh.set_varbits(['10151'])
    qh.set_player_world_location()
    qh.set_inventory()
    qh.set_canvas()
    qh.set_skills({'hitpoints', 'strength', 'ranged', 'magic', 'attack', 'defence', 'prayer'})
    qh.set_widgets({'233,0', '541,23', '541,22', '541,21', '161,62', osrs.widget_ids.run_energy_widget_id, '541,25'})
    # Pillar overlay
    qh.set_widgets({'413,1', '413,6', '413,7', '413,8', '413,9', '413,15', '413,21', '413,27'})
    qh.set_active_prayers()
    qh.set_interating_with()
    qh.set_equipment()
    qh.set_canvas()
    qh.set_right_click_menu()
    anchor = None
    pots = osrs.combat_utils.PotConfig(prayer=True, super_str=True, super_atk=True).asdict()
    while True:
        qh.query_backend()
        (pnm, nw_totem, se_totem, sw_totem, ne_totem, nw_totem_charged,
         se_totem_charged, sw_totem_charged, ne_totem_charged, sleepwalker) = npc_parser(qh)
        # handle sleep walkers immediately!!
        if sleepwalker:
            sleepwalker_handler()
            continue
        # load in the arena tiles
        if anchor:
            qh.clear_tiles()
            qh.set_tiles(set(
                osrs.util.generate_surrounding_tiles_from_point(12, anchor)
            ))
        claw_tile = osrs.util.find_closest_target_in_game(
            qh.get_objects_v2('graphics', 1767),
            qh.get_player_world_location(),
            lambda obj: obj['x_coord'] == qh.get_player_world_location('x') and obj[
                'y_coord'] == qh.get_player_world_location('y') and obj['animation'] <= 50
        )
        any_claws = osrs.util.find_closest_target_in_game(
            qh.get_objects_v2('graphics', 1767),
            qh.get_player_world_location(),
            lambda obj: obj['animation'] <= 65
        )
        spore_tile = osrs.util.find_closest_target_in_game(
            (qh.get_objects_v2('game', 37739) or []) + (qh.get_objects_v2('game', 37738) or []),
            qh.get_player_world_location(),
            lambda obj: obj['dist'] <= 1
        )
        any_spore = osrs.util.find_closest_target_in_game(
            (qh.get_objects_v2('game', 37739) or []) + (qh.get_objects_v2('game', 37738) or []),
            qh.get_player_world_location()
        )
        # phosani wont attack me w spores out so just turn off prayer
        if spore_tile and qh.get_active_prayers():
            osrs.player.flick_all_prayers()

        pillar_overlay = qh.get_widgets('413,1')
        # set my anchor tile
        if pnm and not anchor:
            anchor = {'x': pnm['x_coord'] + 2, 'y': pnm['y_coord'] + 2, 'z': 3}
            osrs.dev.logger.info("Settting PNM anchor tile: %s", anchor)

        safe_tiles = find_safe_quadrant(
            (qh.get_objects_v2('game', 37743) or []) +
            (qh.get_objects_v2('game', 37744) or []) +
            (qh.get_objects_v2('game', 37745) or []),
            anchor,
            osrs.util.combine_objects(qh.get_tiles())
        )
        bad_tiles = add_phosanis_tiles(set(), pnm)
        quadrant_attack = len(osrs.util.combine_objects(qh.get_tiles())) != len(safe_tiles)
        if (claw_tile or spore_tile or quadrant_attack
                or (
                        f"{qh.get_player_world_location('x')},{qh.get_player_world_location('y')}" in bad_tiles
                        and pillar_overlay
                )
        ):
            bad_tiles = add_unsafe_claw_tiles(bad_tiles, qh.get_objects_v2('graphics', 1767))
            pillars = ([] + [ne_totem] + [nw_totem] + [se_totem] + [sw_totem] + [ne_totem_charged] +
                       [nw_totem_charged] + [se_totem_charged] + [sw_totem_charged])
            pillars = list(filter(
                lambda item: item is not None,
                pillars
            ))
            bad_tiles = add_pillar_tiles(bad_tiles, pillars)
            # dont stand next to any of the yawning spores
            if qh.get_objects_v2('game', 37739):
                bad_tiles = add_unsafe_spore_tiles(bad_tiles, qh.get_objects_v2('game', 37739))
            elif qh.get_objects_v2('game', 37738):
                bad_tiles = add_unsafe_spore_tiles(bad_tiles, qh.get_objects_v2('game', 37738))
            nearby_tiles = osrs.util.combine_objects(qh.get_tiles())
            # filter out the tiles that are dangerous
            nearby_tiles = [tile for tile in nearby_tiles if f"{tile['x_coord']},{tile['y_coord']}" not in bad_tiles]
            # filter out the tiles that are outside the game arena
            # this will ensure the tile i am stepping on is no more than 9 tiles away from the center
            # and should be safe since the arena is 20 x 20
            nearby_tiles = [
                tile for tile in nearby_tiles if abs(tile['x_coord'] - anchor['x']) < 9
                                                 and abs(tile['y_coord'] - anchor['y']) < 9
            ]
            # further filter by safe quadrant because we are under a quadrant attack
            nearby_tiles = find_safe_quadrant(
                (qh.get_objects_v2('game', 37743) or []) +
                (qh.get_objects_v2('game', 37744) or []) +
                (qh.get_objects_v2('game', 37745) or []),
                anchor,
                nearby_tiles
            )
            # get the tiles around phosani
            pnm_perim = osrs.util.monster_perimeter_coordinates(7, pnm, 3)
            preferred_tiles = [tile for tile in nearby_tiles if f"{tile['x_coord']},{tile['y_coord']},3" in pnm_perim]
            closest_preferred_tile = osrs.util.find_closest_target_in_game(
                preferred_tiles,
                qh.get_player_world_location()
            )

            '''if pillar_overlay:
                return'''
            # no need to be close to phosani when i am attacking the pillars
            if closest_preferred_tile and closest_preferred_tile['dist'] <= 2 and not qh.get_widgets('413,1'):
                osrs.dev.logger.info("Found a tile on phosanis perimeter")
                # i right click here because sometimes quickly clicking will wind up clicking phosani and stalling my run
                # which will cause me to get hit by a portal
                osrs.move.go_to_loc(
                    closest_preferred_tile['x_coord'], closest_preferred_tile['y_coord'], 3,
                    skip_dax=True, exact_tile=True, right_click=True
                )
            else:
                osrs.dev.logger.info("No tile on phosanis perimeter safe - finding a safe tile elsewhere. %s, %s, %s",
                                     pnm_perim, preferred_tiles, nearby_tiles)
                closest_safe_tile = osrs.util.find_closest_target_in_game(
                    nearby_tiles,
                    qh.get_player_world_location()
                )
                osrs.move.go_to_loc(closest_safe_tile['x_coord'], closest_safe_tile['y_coord'], 3, skip_dax=True,
                                    exact_tile=True)
            qh.query_backend()

        curse_start = curse_handler(qh)

        # Handle pnm's direct attacks
        if pnm and pnm['animation'] == 8594:
            osrs.dev.logger.debug("Phosani is about to melee me.")
            if curse_start:
                osrs.combat_utils.prayer_handler(qh, ['protect_range'])
            else:
                osrs.combat_utils.prayer_handler(qh, ['protect_melee'])
        elif pnm and pnm['animation'] == 8595:
            osrs.dev.logger.debug("Phosani is about to mage me.")
            if curse_start:
                osrs.combat_utils.prayer_handler(qh, ['protect_melee'])
            else:
                osrs.combat_utils.prayer_handler(qh, ['protect_mage'])
        elif pnm and pnm['animation'] == 8596:
            osrs.dev.logger.debug("Phosani is about to range me.")
            if curse_start:
                osrs.combat_utils.prayer_handler(qh, ['protect_mage'])
            else:
                osrs.combat_utils.prayer_handler(qh, ['protect_range'])
        elif not pnm:
            osrs.dev.logger.debug("phosani not found")

        if qh.get_varbits('10151'):
            osrs.dev.logger.warning("i am diseased")
            if qh.get_inventory(disease_pots):
                osrs.move.fast_click_v2(qh.get_inventory(disease_pots))

        osrs.combat_utils.fast_food_handler(qh, 55)
        osrs.combat_utils.pot_handler(qh, pots, 25, 35)

        husk_present = husk_handler(qh)
        parasite_present = None
        if not any_claws:
            parasite_present = parasite_handler(qh, qh.get_interating_with(), claw_tile)

        if husk_present or parasite_present:
            continue

        if pnm and pnm['animation'] == 8609:
            pnm_area = osrs.util.determine_large_monster_area(pnm, 5)
            segment_attack = False
            for tile in pnm_area:
                if tile['x_coord'] == anchor['x'] and tile['y_coord'] == anchor['y']:
                    segment_attack = True
            if not segment_attack:
                osrs.dev.logger.warning("Phosani is preparing a wave dash attack.")
                wave_dash_handler(pnm, anchor, qh)

        # look for something to attack!
        if not qh.get_interating_with() and not husk_present and not parasite_present:
            # we should be attacking pnm because he is not asleep(8613) and pillars arent attackable
            if pnm and pnm['poseAnimation'] != 8613 and not pillar_overlay:
                # there are claws out and attacking pnm would cause me to change tiles, wait until its safe to attack
                if any_claws:
                    pnm_perim = osrs.util.monster_perimeter_coordinates(7, pnm, 3)
                    if f"{qh.get_player_world_location('x')},{qh.get_player_world_location('y')},3" not in pnm_perim:
                        osrs.dev.logger.info("Claws are out and I am not along pnm's perimeter - skipping an attack")
                        continue
                osrs.dev.logger.info("attacking phosani")
                osrs.player.equip_item_no_wait([osrs.item_ids.ZOMBIE_AXE], qh.get_equipment())
                osrs.move.conditional_click(
                    qh, pnm, 'Attack'
                )
            # we should be attacking pillars right now
            elif pillar_overlay:
                osrs.player.equip_item_no_wait([osrs.item_ids.TRIDENT_OF_THE_SWAMP], qh.get_equipment())
                target_pillar = determine_pillar_to_attack(
                    qh, nw_totem, ne_totem, se_totem, sw_totem, any_spore
                )
                # a pillar is visible to attack
                if target_pillar and 'name' in target_pillar and target_pillar['dist'] <= 6:
                    osrs.move.conditional_click(
                        qh,
                        target_pillar,
                        'Charge',
                        target_field='id'
                    )
                elif not any_spore and not any_claws and not quadrant_attack:
                    # pillar is up but not on screen - walk towards these coords
                    if target_pillar and 'name' not in target_pillar:
                        osrs.move.fast_click_v2(qh.get_tiles(
                            f"{target_pillar['x_coord']},{target_pillar['y_coord']},3"))
                    elif target_pillar and 'name' in target_pillar:
                        osrs.move.conditional_click(
                            qh,
                            target_pillar,
                            'Charge',
                            target_field='id'
                        )


#go_to_nightmare()
main()

'''
notes


potentially try to pray against the husks
need to figure out what graphics object is under phosani when he does the claw phase so that when attacking pillars i know to move if im under him 

not always catching when phosani curse is lifted if too many chats come in at the same time
'''
