import random

import osrs
import datetime

loot_sack = '22531'
broad_unf = '11876'
feather = '314'

def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_skills({'fletching'})
    while True:
        qh.query_backend()
        if qh.get_skills('fletching')['level'] == 99:
            exit('99')
        else:
            print(qh.get_skills('fletching')['level'])
        if random.randint(1, 100) == 1:
            osrs.clock.random_sleep(3, 4)
            continue
        if qh.get_inventory(feather) and qh.get_inventory(broad_unf):
            osrs.move.fast_click(qh.get_inventory(broad_unf))
            osrs.move.fast_click(qh.get_inventory(feather))

main()
