import osrs


def main():
    qh = osrs.queryHelper.QueryHelper()
    qh.set_game_objects(
        {'2528,3371,0'},
        {'6', '14916'}
    )
    while True:
        osrs.clock.random_sleep(17, 24)
        qh.query_backend()
        if qh.get_game_objects('6'):
            osrs.move.click(qh.get_game_objects('6')[0])
        elif qh.get_game_objects('14916'):
            osrs.move.click(qh.get_game_objects('14916')[0])

