import osrs
import datetime

loot_sack = '22531'
#closest = osrs.util.find_closest_npc(knight)
seeds = [
    22879,
    5100,
    5104,
    5105,
    5106,
    5264,
    5295,
    5296,
    5297,
    5298,
    5299,
    5300,
    5301,
    5302,
    5303,
    5304,
    5291,
    5293
]

script_config = {
    'intensity': 'high',
    'login': lambda: osrs.clock.random_sleep(4, 5),
    'logout': lambda: osrs.clock.random_sleep(11, 14),
}


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_npcs(['5730'])
    qh.set_skills({'hitpoints', 'thieving'})
    while True:
        qh.query_backend()
        osrs.game.break_manager_v4(script_config)
        if qh.get_skills('hitpoints') and qh.get_skills('hitpoints')['boostedLevel'] < 20:
                exit('no food')
        elif len(qh.get_inventory()) == 28:
            for item in qh.get_inventory():
                if int(item['id']) not in seeds:
                    osrs.move.fast_click(item)
                    osrs.clock.random_sleep(0.1, 0.11)
        else:
            closest = osrs.util.find_closest_npc(qh.get_npcs())
            if closest:
                if 'overheadText' in closest and closest['overheadText'] == 'What do you think you\'re doing?':
                    osrs.clock.random_sleep(2, 2.4)
                    continue
                else:
                    osrs.move.fast_click(closest)

main()
