import pickle
import os

movements = []
for file in os.listdir('C:\\Users\\gland\\osrs_yolov3\\chopper\\north_'):
    if "north" in file:
        unpickled = open('C:\\Users\\gland\\osrs_yolov3\\chopper\\north_\\' + file, "rb")
        savedMovements = pickle.load(unpickled)
        movements.append(savedMovements)
print('movements', movements, len(movements))