import osrs


def bank(qh, task_started, equipment, supplies):
    if not osrs.bank.banking_handler(None, check_bank_in_sight=True):
        osrs.move.go_to_loc(3185, 3436, exact_tile=True)
    items_to_withdraw = supplies if task_started else [] + equipment + supplies
    qh.query_backend()
    osrs.dev.logger.info('starting task.')
    '''
    once leagues starts i should add any new items i need here to replace other items i always have like
    the rune pouch. i can just withdraw laws, airs, waters, fires, and earths and ignore the rune pouch
    '''
    success = osrs.bank.banking_handler({
        'dump_inv': True,
        'dump_equipment': not task_started,
        'search': [{'query': 'slayer', 'items': items_to_withdraw}]
    })
    if not success:
        print('failed to withdraw supplies.')
        exit(4)