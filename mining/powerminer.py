import osrs

import osrs

def main():
    curr_rock = 0
    while True:
        while True:
            clicked = False
            data = osrs.server.get_player_info(7776)
            if data["rockData"]:
                for rock in data["rockData"]:
                    print(rock)
                    if rock["num"] == (curr_rock % 3):
                        osrs.move.move_and_click(rock["x"], rock["y"], 7, 7)
                        clicked = True
                        curr_rock += 1
                        break
                if clicked:
                    break
                osrs.clock.random_sleep(1, 2)
        osrs.move.bezier_movement(1721,  753, 1874, 802)
        # wait for the rock to be mined
        found_ore = False
        osrs.clock.antiban_rest(100, 300, 500)
        while True:
            data = osrs.server.get_player_info(7776)
            if data["inv"]:
                for item in data["inv"]:
                    if item["id"] == 440:
                        osrs.move.move_and_click(item["x"], item["y"], 5, 5)
                        found_ore = True
                if found_ore:
                    break
        osrs.clock.antiban_rest(100, 300, 500)
main()