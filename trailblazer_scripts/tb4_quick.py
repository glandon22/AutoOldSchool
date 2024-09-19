import osrs


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_inventory()
    while True:
        qh.query_backend()
        count = qh.get_inventory()[0]['quantity']
        osrs.move.click(qh.get_inventory()[0])
        osrs.move.click({'x': qh.get_inventory()[0]['x'] - 250, 'y': qh.get_inventory()[0]['y']})
        osrs.clock.random_sleep(2.3, 2.4)
        osrs.move.click({'x': qh.get_inventory()[0]['x'] - 250, 'y': qh.get_inventory()[0]['y']})
        qh.query_backend()
        if qh.get_inventory()[0]['quantity'] != count:
            osrs.clock.random_sleep(1.3, 1.4)
        else:
            osrs.clock.random_sleep(4, 4.1)

main()