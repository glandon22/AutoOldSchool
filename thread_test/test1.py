import datetime

import osrs
from combat import slayer_killer

pot_config = slayer_killer.PotConfig(super_combat=True)
from osrs.item_ids import ItemIDs


def monkfish_eval(loot_priority):
    if loot_priority > 5:
        return True
    qh = osrs.queryHelper.QueryHelper()
    qh.set_skills({'hitpoints'})
    qh.query_backend()
    if qh.get_skills('hitpoints')['level'] - qh.get_skills('hitpoints')['boostedLevel'] > 12:
        return True
    return False

dl = osrs.loot.LootConfig(osrs.item_ids.ItemIDs.EYE_OF_NEWT.value, 6)
monkfish = osrs.loot.InvConfig(osrs.item_ids.ItemIDs.MONKFISH.value, monkfish_eval, left_click=False)
loot = osrs.loot.Loot()
loot.add_item(dl)
loot.add_inv_config_item(monkfish)
# this doesnt pick up multiple things in one trip right yet

print(loot.retrieve_loot(10))