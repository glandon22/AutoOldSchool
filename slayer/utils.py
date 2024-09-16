import osrs


def bank(qh, task_started, equipment, supplies):
    items_to_withdraw = supplies if task_started else [] + equipment + supplies
    qh.query_backend()
    osrs.dev.logger.info('starting blue dragons task.')
    success = osrs.bank.banking_handler({
        'dump_inv': True,
        'dump_equipment': not task_started,
        'withdraw_v2': items_to_withdraw
    })
    if not success:
        print('failed to withdraw supplies.')
        exit(4)