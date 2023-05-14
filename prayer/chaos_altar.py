import keyboard

from autoscape import general_utils

### Work in progress
def main():
    general_utils.move_and_click(800, 800, 9, 9)
    keyboard.send('f4')
    general_utils.random_sleep(1, 1.1)
    loc = general_utils.rough_img_compare('..\\screens\\burning_amulet.png', 0.9, (0, 0, 1920, 1080))
    if not loc:
        return
    general_utils.move_and_click(loc[0], loc[1], 5, 5, 'right')
    general_utils.random_sleep(1, 1.1)
    loc = general_utils.rough_img_compare('..\\screens\\lava_maze.png', .99, (0, 0, 1920, 1080))
    if not loc:
        return
    general_utils.move_and_click(loc[0], loc[1], 2, 2)
    general_utils.random_sleep(1.3, 1.5)
    keyboard.send('1')
    # need to make an api that tells my world position, and instead of just sleeping
    # let me know when i am in wildy tile: 3026, 3840, 0
    while True:
        general_utils.move_and_click(1777, 95, 7, 7)
        general_utils.random_sleep(1, 2)

    # run west until x: 2960 ish maybe a little higher
    # check for wall object ids 1521 or 1524, if so door is closed and needs to be opened (2958, 3820, 0) and (2958, 3821, 0)
    # find chaos altar id 411 (2947, 3820, 0)
    # use item 523 on altar big bones
        # if level, do this again
    # when bag has no bones look for wine of zammy id 245 and spam click, after first click,
    # wait a few seconds then find coords again and spam click wine of zammy counts as a ground item i believe
    # need to determine when im dead
    # wait til i spawn in lumby 3223, 3219, 0
    # right click ring of wealth and tele to ge
    # equip jewelry
    # get bones
    #repeat

main()
