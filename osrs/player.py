import osrs.move as move
import osrs.server as server
import osrs.dev as dev

def toggle_prayer_slow(desired_state, port):
    """
    :param desired_state: string : 'on' : 'off'
    :param port:
    :return: void
    """
    desired_state = {'on': 1066, 'off': 1063}[desired_state]
    while True:
        prayer_orb = server.get_widget('160,21', port)
        if prayer_orb:
            if prayer_orb['spriteID'] != desired_state:
                move.move_and_click(prayer_orb['x'], prayer_orb['y'], 3, 3)
            return


def toggle_prayer(desired_state, port='56799'):
    """
    :param desired_state: string : 'on' : 'off'
    :param port:
    :return: void
    """
    desired_state = {'on': 1066, 'off': 1063}[desired_state]
    while True:
        prayer_orb = server.get_widget('160,21', port)
        if prayer_orb:
            if prayer_orb['spriteID'] != desired_state:
                move.fast_move_and_click(prayer_orb['x'], prayer_orb['y'], 3, 3)
            return


def toggle_run(desired_state, port):
    """
    :param desired_state: string : 'on' : 'off'
    :param port:
    :return: void
    """
    desired_state = {'on': 1065, 'off': 1064}[desired_state]
    while True:
        run_orb = server.get_widget('160,29', port)
        if run_orb:
            if run_orb['spriteID'] != desired_state:
                move.fast_move_and_click(run_orb['x'], run_orb['y'], 3, 3)
            return


def get_run_energy():
    while True:
        dev.app_log.info('getting run energy.')
        run_orb = server.get_widget('160,28')
        if run_orb:
            dev.app_log.info('got run energy: {}'.format(run_orb))
            return int(run_orb['text'])
