import random
import osrs.server as server
import osrs.clock as clock
import osrs.move as move


def handle_marks(x_min, x_max, y_min, y_max, z, port):
    retries = 0
    while retries < random.randint(3, 8):
        marks = server.get_ground_items_in_coords(x_min, x_max, y_min, y_max, z, ['11849'], port)
        if '11849' in marks:
            loc = server.get_world_location(port)
            if 'x' in loc and x_min <= loc['x'] <= x_max and y_min <= loc['y'] <= y_max and loc['z'] == z:
                move.move_and_click(marks['11849'][0]['x'], marks['11849'][0]['y'], 2, 3)
                clock.random_sleep(0.5, 0.6)
                move.wait_until_stationary()
                retries += 1
            else:
                break
        else:
            break