import datetime

import keyboard

from fishing import catch_fish
from autoscape import general_utils

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
    general_utils.random_sleep(10, 15)
    while True:
        start_time = general_utils.multi_break_manager(start_time, 53, 58, 423, 551, acc_configs)
        catch_fish('2', '56799')
        general_utils.random_sleep(0.5, 0.6)
        keyboard.send('alt + tab')
        general_utils.random_sleep(0.5, 0.6)
        catch_fish('2', '56800')
        general_utils.random_sleep(0.5, 0.6)
        keyboard.send('alt + tab')
        general_utils.random_sleep(0.5, 0.6)


main()
