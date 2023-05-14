from autoscape import general_utils
port = '56799'
brothers_status = {
    'dh': 0,
    'v': 0,
    'tor': 0,
    'kar': 0,
    'guth': 0,
    'ah': 0,
}
spade_id = 952

#pray prb 160,20
# graphics id will not be equal to -1 for the monster i am supposed to kill will be equal to 1253, it flickers so will need to do while loop
def kill_dharok():
    general_utils.run_towards_square({'x': 3575, 'y': 3298, 'z': 0}, port)
    inv = general_utils.get_inv(port)
    spade = general_utils.is_item_in_inventory_v2(inv, spade_id)
    if not spade:
        exit('no spade')
    general_utils.move_and_click(spade['x'], spade['y'], 3, 3)
    while True:
        loc = general_utils.get_world_location(port)
        if 'z' in loc and loc['z'] == 3:
            break
    general_utils.sleep_one_tick()
    tomb = general_utils.get_surrounding_game_objects(8, [20720])
    if not tomb:
        exit('no dh tomb')
    if '20720' in tomb:
        general_utils.move_and_click(tomb['20720']['x'], tomb['20720']['y'], 2, 2)
        general_utils.random_sleep(2, 2.3)

    # click tomb
    # if monster, kill
    # else see if sll brothers dead, if so enter tunnel
    # else kill other bros

#kill_dharok()
print('g',general_utils.get_npcs_by_id('1673', port))