import osrs

def have_bellows():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.query_backend()
    return osrs.inv.get_item_quantity_in_inv(qh.get_inventory(), osrs.item_ids.OGRE_BELLOWS_3) > 10


def main():
    qh = osrs.queryHelper.QueryHelper()
    # chompy 1475
    qh.set_npcs(['1475', '1473'])
    qh.set_interating_with()
    qh.set_inventory()
    qh.set_player_world_location()
    qh.set_players()
    qh.set_canvas()
    while True:
        osrs.game.break_manager_v4({
            'intensity': 'low',
            'login': False,
            'logout': False
        })
        qh.query_backend()
        chompy = osrs.util.find_closest_target_in_game(
            qh.get_npcs(), qh.get_player_world_location(), lambda npc: npc['id'] == 1475 and npc['health'] != 0
        )
        frogs = osrs.util.find_closest_target_in_game(
            qh.get_npcs(), qh.get_player_world_location(), lambda npc: npc['id'] == 1473
        )
        if qh.get_players() and len(qh.get_players()) > 1:
            osrs.game.hop_worlds(None, True)
        if qh.get_interating_with():
            continue
        if chompy and not qh.get_interating_with() and osrs.move.is_clickable(chompy):
            osrs.move.fast_click_v2(chompy)
        elif not qh.get_inventory([
            osrs.item_ids.OGRE_BELLOWS_1, osrs.item_ids.OGRE_BELLOWS_2, osrs.item_ids.OGRE_BELLOWS_3
        ]):
            osrs.move.interact_with_object_v3(
                684, obj_tile={'x': 2395, 'y': 3046, 'z': 0}, custom_exit_function=have_bellows,
                timeout=3
            )
        elif qh.get_inventory(osrs.item_ids.BLOATED_TOAD):
            osrs.move.fast_click_v2(qh.get_inventory(osrs.item_ids.BLOATED_TOAD))
        elif frogs and not qh.get_interating_with():
            osrs.move.right_click_v6(
                frogs,
                'Inflate',
                qh.get_canvas(),
                in_inv=True
            )

main()