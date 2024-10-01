import osrs
import random
from mining import mlm_upstairs
from agility import frem_v2
from fishing import aerial
from woodcutting import sullys
from farming import bologano_v2, logovano_v3

'''
{
    'func': bologano_v2.main, 'args': [False]
},
    
    '''

config = [
    {
        'func': mlm_upstairs.main, 'args': [False]
    },
    {
        'func': frem_v2.main, 'args': [99, False]
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
]


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