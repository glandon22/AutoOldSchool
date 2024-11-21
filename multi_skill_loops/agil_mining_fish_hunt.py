import osrs
import random
from mining import mlm_upstairs, powerminer_v2
from agility import frem_v2, ardy_v3
from fishing import aerial
from woodcutting import sullys
from farming import bologano_v2, logovano_v3
from firemaking import wt
from slayer import index as slayer_loop

'''
{
    'func': bologano_v2.main, 'args': [False]
},
{
    'func': slayer_loop.main, 'args': [False]
},
{
    'func': powerminer_v2.main, 'args': [False, 'iron']
},
'''

config = [
    {
        'func': mlm_upstairs.main, 'args': [False]
    },
    {
        'func': ardy_v3.main, 'args': [99, False]
    },
    {
        'func': aerial.main, 'args': [False]
    },
    {
        'func': sullys.main, 'args': [False]
    },
    {
        'func': logovano_v3.main, 'args': [False]
    },
    {
        'func': wt.main, 'args': [False]
    },
]

'''config = [
    {
        'func': slayer_loop.main, 'args': [False]
    },
]'''

def main():
    while True:
        random.shuffle(config)
        osrs.dev.logger.info('Invoking scripts in the following order:')
        for routine in config:
            osrs.dev.logger.info(routine['func'].__module__)
        for routine in config:
            osrs.dev.logger.info('Beginning function: %s with args: %s', routine['func'].__module__, routine['args'])
            routine['func'](*routine['args'])

main()