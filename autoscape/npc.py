import math


def find_closest_npc(npcs, ignore=-1):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for npc in npcs:
        if npc['id'] != ignore and npc["dist"] < closest["dist"]:
            closest = {
                "dist": npc["dist"],
                "x": math.floor(npc["x"]),
                "y": math.floor(npc["y"]),
                "id": npc["id"]
            }
    return closest


def find_an_npc(npcs, min_dist):
    closest = {
        "dist": 999,
        "x": None,
        "y": None,
        "id": None
    }
    for npc in npcs:
        if closest["dist"] > npc["dist"] >= min_dist:
            closest = {
                "dist": npc["dist"],
                "x": math.floor(npc["x"]),
                "y": math.floor(npc["y"]),
                "id": npc["id"]
            }
    if closest['x'] is None:
        return False
    else:
        return closest

