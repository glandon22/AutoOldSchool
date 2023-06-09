
import osrs
wc_animations = [
    879,877,875,873,871,869,867,8303,2846,24,2117,7264,8324,8778
]
# reg logs 1511
# oak log 1521
expected_logs = 1511
#reg trees
# oak tree 10820
# teak
expected_tree = '1276'

def main():
    while True:
        data = osrs.server.get_player_info(6464)
        print(data['gameObjects'])
        if len(data['inv']) == 28:
            print('bag is full')
            osrs.inv.power_drop(data['inv'], [], [expected_logs])
            continue

        # i am no longer chopping
        if data['animation'] not in wc_animations:
            print('no longer chopping')
            if len(data['gameObjects']):
                print('found trees to blast')
                closest = {
                    'x': None,
                    'y': None,
                    'dist': 999
                }
                for tree in data['gameObjects'][expected_tree]:
                    if tree['dist'] == 1:
                        closest = tree
                        break
                    elif closest['dist'] > tree['dist']:
                        closest = tree
                osrs.move.move_and_click(closest['x'], closest['y'], 1, 1)
                osrs.clock.random_sleep(0.3, 0.4)
                osrs.move.click_off_screen()
                # once i click tree, wait to cycle again until i start chopping it
                cycles = 0
                while True:
                    print('waiting to chop tree: ', cycles )
                    data = osrs.server.get_player_info(6464)
                    if data['animation'] in wc_animations or cycles > 60:
                        break
                    cycles += 1
                osrs.clock.random_sleep(1.2, 2.3)
        print('chopping')


main()
