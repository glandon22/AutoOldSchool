from osrs_utils import general_utils
import pyscreenshot
import numpy as np
import keyboard

def chop_highlighted_tree():
    prev_inv = pyscreenshot.grab((2299, 1024, 2510, 1324))
    general_utils.find_fixed_object(np.array(pyscreenshot.grab((0, 0, 2560, 1440))), 0, 0)
    return prev_inv


def did_get_log(prev_inv):
    while True:
        curr_inv = pyscreenshot.grab((2299, 1024, 2510, 1324))
        if general_utils.calc_img_diff(prev_inv, curr_inv, 1) == 'different':
            break


def main():
    while True:
        inv = None
        while True:
            try:
                inv = chop_highlighted_tree()
                break
            except TypeError:
                continue
        print('here')
        did_get_log(inv)
        print('here1')
        if general_utils.is_bag_full():
            process = general_utils.process_with_tool(1, '1', '..\\screens\\empty_bag\\slot27.png', 35)
            if process != 'success':
                return print(process)


main()
