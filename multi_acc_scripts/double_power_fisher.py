import datetime

import keyboard

from fishing import catch_fish

import osrs

acc_configs = [
    {
        'port': '56799',
        'password': 'pass_70',
        'post_login_steps': None
    },
    {
        'port': '56800',
        'password': 'pass_71',
        'post_login_steps': None
    }
]


def main():
    start_time = datetime.datetime.now()
    osrs.clock.random_sleep(10, 15)
    while True:
        start_time = osrs.game.multi_break_manager(start_time, 53, 58, 423, 551, acc_configs)
        catch_fish('2', '56799')
        osrs.clock.random_sleep(0.5, 0.6)
        keyboard.send('alt + tab')
        osrs.clock.random_sleep(0.5, 0.6)
        catch_fish('2', '56800')
        osrs.clock.random_sleep(0.5, 0.6)
        keyboard.send('alt + tab')
        osrs.clock.random_sleep(0.5, 0.6)


main()
