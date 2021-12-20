import mouse
import datetime
import pickle
import time

mouse.move(1311,454)
currTime = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
print('----------------------------------------------------------------------------------------recording in 3')
time.sleep(1)
print('----------------------------------------------------------------------------------------recording in 2')
time.sleep(1)
print('----------------------------------------------------------------------------------------recording in 1')
time.sleep(1)
print('----------------------------------------------------------------------------------------move now')
mouseMovements = mouse.record(button='left', target_types=('double',))
with open("north_/north_" + currTime + ".txt", "wb") as north_tree:
    for movements in mouseMovements:
        pickle.dump(mouseMovements, north_tree)