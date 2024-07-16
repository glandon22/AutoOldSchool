import datetime
import random
import logging
import osrs
import sys

print(sys.argv)

bankers_ids = [
    '1633',
    '1613',
    '1634',
    '3089'
]

#POT = int(sys.argv[1])
#SECONDARY = int(sys.argv[2])

script_config = {
    'intensity': 'high',
    'login': False,
    'logout': False
}


def main(pot, secondary, goal_level=99):
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    qh.set_bank()
    qh.set_skills({'herblore'})
    qh.set_widgets({'233,0', '270,14'})
    qh.set_npcs(bankers_ids)
    osrs.bank.banking_handler({
        'set_quantity': '14',
        'dump_inv': True,
        'withdraw': [{'items': [pot, secondary]}]
    })
    last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
    last_banked = datetime.datetime.now()
    while True:
        osrs.game.break_manager_v4(script_config)
        qh.query_backend()
        if qh.get_skills('herblore') and qh.get_skills('herblore')['level'] >= goal_level:
            return
        pot_object = qh.get_inventory(pot)
        secondary_object = qh.get_inventory(secondary)
        if (not secondary_object or not pot_object) and (datetime.datetime.now() - last_banked).total_seconds() > 2:
            osrs.bank.banking_handler({
                'dump_inv': True,
                'withdraw': [{'items': [pot, secondary]}]
            })
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)
            last_banked = datetime.datetime.now()
        elif pot_object and secondary_object and (datetime.datetime.now() - last_click).total_seconds() > 25:
            osrs.move.click(pot_object)
            osrs.move.click(secondary_object)
            wait_time = datetime.datetime.now()
            while True:
                qh.query_backend()
                if qh.get_widgets('270,14'):
                    osrs.keeb.keyboard.press(osrs.keeb.key.space)
                    osrs.keeb.keyboard.release(osrs.keeb.key.space)
                    last_click = datetime.datetime.now()
                    if random.randint(0, 2) == 1:
                        osrs.move.jiggle_mouse()
                    break
                elif (datetime.datetime.now() - wait_time).total_seconds() > 4:
                    break
        elif qh.get_widgets('233,0'):
            last_click = datetime.datetime.now() - datetime.timedelta(hours=1)

