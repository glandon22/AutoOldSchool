import osrs
import datetime

loot_sack = '22531'
#closest = osrs.util.find_closest_npc(knight)
def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_npcs(['3297', '11936'])
    qh.set_skills({'hitpoints'})
    while True:
        qh.query_backend()
        if qh.get_skills('hitpoints') and qh.get_skills('hitpoints')['boostedLevel'] < 20:
            if qh.get_inventory('3144'):
                osrs.move.click(qh.get_inventory('3144'))
                osrs.clock.sleep_one_tick()
            else:
                exit('no food')
        elif qh.get_inventory(loot_sack) and qh.get_inventory(loot_sack)['quantity'] >= 56:
            osrs.move.click(qh.get_inventory(loot_sack))
            osrs.clock.sleep_one_tick()
        else:
            closest = osrs.util.find_closest_npc(qh.get_npcs())
            if closest:
                if 'overheadText' in closest and closest['overheadText'] == 'What do you think you\'re doing?':
                    osrs.clock.random_sleep(2, 2.4)
                    continue
                else:
                    osrs.move.fast_click(closest)

main()
