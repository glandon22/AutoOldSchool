from autoscape import general_utils

def fally():
    obstacles = [
        [10, 10, 223],
        [35, 76, 35],
        [70, 3, 43],
        [54, 100, 65],
        [100, 0, 0],
        [150, 0, 0],
        [200, 0, 0],
        [0, 50, 0],
        [65, 100, 0],
        [0, 150, 0],
        [0, 200, 21],
        [0, 0, 50],
        [0, 0, 100]
    ]
    for i in range(13):
        # this obstacles needs an extra delay to find the click box
        if i == 6:
            print('at the slow obstacle')
            general_utils.random_sleep(0.6, 0.7)
        if not general_utils.do_obstacle(obstacles[i]):
            general_utils.walk_south_minimap()
            general_utils.wait_until_stationary()
            break
        if general_utils.find_mark():
            general_utils.wait_until_stationary()

while True:
    fally()
    general_utils.antiban_randoms()
    general_utils.antiban_rest()
