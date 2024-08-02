import osrs
KNIFE_ID = 946
FISH_TO_CUT = [
    22826, # bluegill
    22829, # common tench
    22832, # common tench
    22835, # common tench
]


script_config = {
    'intensity': 'high',
    'login': False,
    'logout': False,
}

def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.player_world_location()
    qh.projectiles()
    qh.npcs(['8523'])
    qh.set_players()
    while True:
        qh.query_backend()
        if len(qh.get_players()) > 1:
            print('alert: ', qh.get_players())
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value))
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value))
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.VARROCK_TELEPORT.value))
        osrs.game.break_manager_v4(script_config)
        fishing_spots = qh.get_npcs()
        if qh.get_inventory(FISH_TO_CUT):
            osrs.move.fast_click(qh.get_inventory(osrs.item_ids.ItemIDs.KNIFE.value))
            osrs.move.fast_click(qh.get_inventory(FISH_TO_CUT))
        # fishing spots are available and my bird is not flying
        elif fishing_spots and len(qh.get_projectiles()) == 0:
            c = osrs.util.find_closest_target(fishing_spots)
            if c and 'x' in c and 'y' in c:
                osrs.move.fast_click(c)


main()
