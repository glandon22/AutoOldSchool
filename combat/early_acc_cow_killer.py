import osrs
from combat.slayer_killer import find_next_target


def main(required_runes: list, darts: int):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_npcs_by_name(['cow'])
    qh.set_skills({'hitpoints'})
    qh.set_interating_with()
    qh.set_equipment()
    ranging = False
    while True:
        osrs.keeb.press_key('space')
        qh.query_backend()
        if not ranging:
            for rune in required_runes:
                if not qh.get_inventory(rune['id']) or qh.get_inventory(rune['id'])['quantity'] < rune['quantity']:
                    if qh.get_inventory(darts):
                        osrs.move.click(qh.get_inventory(darts))
                        osrs.clock.sleep_one_tick()
                        ranging = True
                    else:
                        return

        elif ranging and not qh.get_equipment(darts):
            return

        if not qh.get_interating_with():
            if qh.get_skills('hitpoints') and qh.get_skills('hitpoints')['boostedLevel'] <= 9:
                if qh.get_inventory(osrs.item_ids.ItemIDs.TROUT.value):
                    osrs.move.click(qh.get_inventory(osrs.item_ids.ItemIDs.TROUT.value))
                else:
                    return
            osrs.game.break_manager_v4({
                'intensity': 'high',
                'login': False,
                'logout': lambda: osrs.clock.random_sleep(11, 11.1)
            })
            if qh.get_npcs_by_name():
                c = find_next_target(qh.get_npcs_by_name(), 'cow', False, None)
                if c:
                    osrs.move.fast_click(c)
