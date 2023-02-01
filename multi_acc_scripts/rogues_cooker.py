import datetime
from cooking import cook_handler
from osrs_utils import general_utils
'''
{
    'port': '56800',
    'password': 'pass_71',
    'post_login_steps': None
}'''
acc_configs = [
    {
        'port': '56799',
        'password': 'pass_70',
        'post_login_steps': None
    }
]


def main():
    start_time = datetime.datetime.now()
    general_utils.random_sleep(10, 15)
    while True:
        start_time = general_utils.multi_break_manager(start_time, 53, 58, 423, 551, acc_configs)
        cook_handler(acc_configs[0]['port'])
        general_utils.random_sleep(0.5, 0.6)
        '''keyboard.send('alt + tab')
        general_utils.random_sleep(0.5, 0.6)
        cook_handler(acc_configs[1]['port'])
        general_utils.random_sleep(0.5, 0.6)
        keyboard.send('alt + tab')
        general_utils.random_sleep(0.5, 0.6)'''

main()
