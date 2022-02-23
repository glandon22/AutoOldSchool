import math
import time

import keyboard
import pyautogui
import pyscreenshot

from osrs_utils import general_utils
required_items = [2132, 2134, 2136, 2138, 3853]

def main():
    started = start_quest()
    if started != 'success':
        return started
    general_utils.random_sleep(3, 3.1)
    talk_to_sanfew()
    general_utils.random_sleep(3, 3.1)
    walk_to_cauldron()
    general_utils.random_sleep(3, 3.1)
    enchant_meat()
    general_utils.random_sleep(3, 3.1)
    back_to_taverley()
    general_utils.random_sleep(3, 3.1)
    return_to_sanfew()
    general_utils.random_sleep(3, 3.1)
    return_to_kaqemeex()
    return

def verify_items():
    # will only work with a games necklace with 8 charges
    inv = general_utils.get_player_info(1489)["inv"]
    games_necklace = [0,0]
    for req in required_items:
        found = False
        for item in inv:
            if req == item["id"]:
                found = True

            if item["id"] == 3853:
                games_necklace = [item["x"], item["y"]]
        if not found:
            return False
    return games_necklace


def start_quest():
    # will need to add tele to burthorpe on games necklace here 3510[1830, 1844, 166, 176]
    v = verify_items()
    if not v:
        return 'missing items'
    general_utils.move_and_click(v[0] + 5, v[1] + 5, 3, 3, 'right')
    general_utils.random_sleep(0.5, 0.7)
    rub = general_utils.rough_img_compare('..\\screens\\rub.png', .99, (0, 0, 1920, 1080))
    if not rub:
        return print('couldnt tele on games necklace')
    general_utils.move_and_click(rub[0] + 3, rub[1] + 3, 1, 1)
    general_utils.random_sleep(1.0, 1.2)
    burthorpe = general_utils.rough_img_compare('..\\screens\\burthorpe.png', .99, (0, 0, 1920, 1080))
    if not burthorpe:
        return print('didnt see burthorpe tele option')
    general_utils.move_and_click(burthorpe[0] + 3, burthorpe[1] + 3, 3, 3)
    # south east
    while True:
        general_utils.move_and_click(1875, 154, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["y"] < 3520:
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    while True:
        # south
        general_utils.move_and_click(1837, 170, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["y"] < 3500:
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # find quest start npc
    dialogue = None
    while True:
        npcs = general_utils.get_player_info(1489)["npcs"]
        click = False
        if len(npcs):
            for npc in npcs:
                if npc["name"] == 'Kaqemeex':
                    pyautogui.moveTo(npc["x"], npc["y"])
                    general_utils.random_sleep(0.1, 0.15)
                    pyautogui.click()
                    general_utils.wait_until_stationary()
                    general_utils.random_sleep(1, 1.1)
                    dialogue = general_utils.rough_img_compare('..\\screens\\quests\\druidic_ritual\\start.png', .75, (0, 0,1920, 1080))
                    print('looking for dialogue', dialogue)
                    general_utils.random_sleep(1.2, 1.3)
                    if dialogue:
                        click = True
                        break
            if click:
                break
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('2')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('1')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    return 'success'

def talk_to_sanfew():
    # walk west
    while True:
        # west
        general_utils.move_and_click(1777, 95, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["x"] < 2897:
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # walk south
    while True:
        # south
        general_utils.move_and_click(1837, 170, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["y"] < 3435:
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # find the stairs
    ######
    ## did not successfully climb stairs
    ######
    # find stairs
    while True:
        found_stairs = False
        objs = general_utils.get_player_info(1489)["objects"]
        print('objs', objs)
        if len(objs):
            for obj in objs:
                if obj["Id"] == 16671:
                    general_utils.move_and_click(1845, 104, 7, 7)
                    found_stairs = True
                    general_utils.random_sleep(3, 3.1)
        if found_stairs:
            break
    general_utils.random_sleep(3, 4)
    # click stairs
    while True:
        objs = general_utils.get_player_info(1489)["objects"]
        if len(objs):
            for obj in objs:
                if obj["Id"] == 16671:
                    general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 2, 2)
                    general_utils.random_sleep(7, 7.1)
        data = general_utils.get_player_info(1489)
        if data['world']['z'] == 1:
            break

    while True:
        print('down')
        npcs = general_utils.get_player_info(1489)["npcs"]
        click = False
        if len(npcs):
            for npc in npcs:
                if npc["name"] == 'Sanfew':
                    pyautogui.moveTo(npc["x"], npc["y"])
                    general_utils.random_sleep(0.1, 0.15)
                    pyautogui.click()
                    general_utils.wait_until_stationary()
                    general_utils.random_sleep(1, 1.1)
                    dialogue = general_utils.rough_img_compare('..\\screens\\quests\\druidic_ritual\\sanfew_1.png', .75, (0, 0,1920, 1080))
                    print('looking for dialogue', dialogue)
                    general_utils.random_sleep(1.2, 1.3)
                    if dialogue:
                        click = True
                        break
            if click:
                break
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('1')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('1')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    # find the stairs
    found_stairs = False
    while True:
        objs = general_utils.get_player_info(1489)["objects"]
        if len(objs):
            for obj in objs:
                if obj["Id"] == 16673:
                    general_utils.wait_until_stationary()
                    general_utils.random_sleep(.7, .9)
                    if found_stairs:
                        general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 7, 7)
                        general_utils.random_sleep(1.2, 1.3)
                        found_stairs = 'complete'
                        break
                    else:
                        found_stairs = True
            if found_stairs == 'complete':
                break

def walk_to_cauldron():
    # walk south
    while True:
        # south
        general_utils.move_and_click(1837, 170, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["y"] < 3400:
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # middle of minimap
    general_utils.move_and_click(1845, 104, 7, 7)
    general_utils.wait_until_stationary()
    general_utils.random_sleep(7, 7.1)
    while True:
        objs = general_utils.get_player_info(1489)["objects"]
        clicked = False
        if len(objs):
            for obj in objs:
                if obj["Id"] == 16680:
                    general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 7, 7)
                    general_utils.random_sleep(1.2,1.3)
                    clicked = True
                    break
            if clicked:
                break
    general_utils.random_sleep(7, 8)
    #walk up to the cauldron
    while True:
        # north
        general_utils.move_and_click(1837, 41, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["y"] > 9815:
            general_utils.wait_until_stationary()
            general_utils.random_sleep(0.7, 0.9)
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    thru_gate = False
    clicked = False
    while True:
        data = general_utils.get_player_info(1489)
        objs = data["objects"]
        if len(objs):
            for obj in objs:
                if obj["Id"] == 2143:
                    print('found door')
                    if not clicked:
                        print('clicking door 1')
                        general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 7, 7)
                        general_utils.wait_until_stationary()
                        clicked = True
                    else:
                        data1 = general_utils.get_player_info(1489)
                        print('d1', data1)
                        if data1["world"]["x"] > 2888:
                            print('thru door')
                            thru_gate = True
                            break
                        else:
                            print('spam clicking door')
                            general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 7, 7)
                            general_utils.random_sleep(0.2, 0.3)
        if thru_gate:
            break

def enchant_meat():
    data = general_utils.get_player_info(1489)
    for item in data["inv"]:
        if item["id"] in required_items:
            objects = general_utils.get_player_info(1489)["objects"]
            cauldron = None
            for obj in objects:
                if obj["Id"] == 2142:
                    cauldron = [math.floor(obj["x"]), math.floor(obj["y"])]
            general_utils.move_and_click(item["x"],item["y"], 5, 5)
            general_utils.random_sleep(0.5, 0.6)
            general_utils.move_and_click(cauldron[0], cauldron[1], 3, 4)
            general_utils.random_sleep(5, 5.1)
            general_utils.random_sleep(0.4, 0.7)

def back_to_taverley():
    objs = general_utils.get_player_info(1489)["objects"]
    if len(objs):
        for obj in objs:
            if obj["Id"] == 2143:
                general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 3, 3)
    while True:
        data = general_utils.get_player_info(1489)
        if data["world"]["x"] <= 2888:
            break
    while True:
        # south
        general_utils.move_and_click(1837, 170, 7, 7)
        general_utils.random_sleep(1, 2)
        print('here')
        data = general_utils.get_player_info(1489)
        print('here1')
        if data and data["world"]["y"] < 9808:
            general_utils.random_sleep(6, 6.1)
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # find ladder
    while True:
        objs = general_utils.get_player_info(1489)["objects"]
        if len(objs):
            for obj in objs:
                if obj["Id"] == 17385:
                    general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 3, 3)
        data = general_utils.get_player_info(1489)
        if data["world"]["y"] <= 3400:
            break
        general_utils.random_sleep(3, 3.1)

def return_to_sanfew():
    # walk north
    while True:
        general_utils.move_and_click(1836, 40, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["y"] > 3420:
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # walk east
    while True:
        general_utils.move_and_click(1900, 109, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["x"] > 2892:
            general_utils.random_sleep(7,7.1)
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # find the stairs
    found_stairs = False
    while True:
        objs = general_utils.get_player_info(1489)["objects"]
        if len(objs):
            for obj in objs:
                if obj["Id"] == 16671:
                    general_utils.wait_until_stationary()
                    general_utils.random_sleep(.7, .9)
                    if found_stairs:
                        general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 7, 7)
                        general_utils.random_sleep(1.2, 1.3)
                        found_stairs = 'complete'
                        break
                    else:
                        found_stairs = True
            if found_stairs == 'complete':
                break

    while True:
        npcs = general_utils.get_player_info(1489)["npcs"]
        click = False
        if len(npcs):
            for npc in npcs:
                if npc["name"] == 'Sanfew':
                    pyautogui.moveTo(npc["x"], npc["y"])
                    general_utils.random_sleep(0.1, 0.15)
                    pyautogui.click()
                    general_utils.wait_until_stationary()
                    general_utils.random_sleep(1, 1.1)
                    dialogue = general_utils.rough_img_compare('..\\screens\\quests\\druidic_ritual\\sanfew_1.png',
                                                               .75, (0, 0, 1920, 1080))
                    print('looking for dialogue', dialogue)
                    general_utils.random_sleep(1.2, 1.3)
                    if dialogue:
                        click = True
                        break
            if click:
                break
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)

def return_to_kaqemeex():
    # find the stairs
    found_stairs = False
    while True:
        objs = general_utils.get_player_info(1489)["objects"]
        if len(objs):
            for obj in objs:
                if obj["Id"] == 16673:
                    general_utils.wait_until_stationary()
                    general_utils.random_sleep(.7, .9)
                    if found_stairs:
                        general_utils.move_and_click(math.floor(obj["x"]), math.floor(obj["y"]), 7, 7)
                        general_utils.random_sleep(1.2, 1.3)
                        found_stairs = 'complete'
                        break
                    else:
                        found_stairs = True
            if found_stairs == 'complete':
                general_utils.random_sleep(2, 2.1)
                break

    # walk north
    while True:
        general_utils.move_and_click(1836, 40, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["y"] > 3473:
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # walk east
    while True:
        general_utils.move_and_click(1900, 109, 7, 7)
        general_utils.random_sleep(1, 2)
        data = general_utils.get_player_info(1489)
        if data and data["world"]["x"] > 2915:
            general_utils.random_sleep(7,7.1)
            break
        else:
            general_utils.random_sleep(1.5, 2.2)
    # find quest start npc
    dialogue = None
    while True:
        npcs = general_utils.get_player_info(1489)["npcs"]
        click = False
        if len(npcs):
            for npc in npcs:
                if npc["name"] == 'Kaqemeex':
                    pyautogui.moveTo(npc["x"], npc["y"])
                    general_utils.random_sleep(0.1, 0.15)
                    pyautogui.click()
                    general_utils.wait_until_stationary()
                    general_utils.random_sleep(1, 1.1)
                    dialogue = general_utils.rough_img_compare('..\\screens\\quests\\druidic_ritual\\start.png', .75, (0, 0,1920, 1080))
                    print('looking for dialogue', dialogue)
                    general_utils.random_sleep(1.2, 1.3)
                    if dialogue:
                        click = True
                        break
            if click:
                break
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('space')
    general_utils.random_sleep(2.1, 2.2)
    keyboard.send('esc')

main()