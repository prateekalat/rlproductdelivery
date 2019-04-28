from environment import Environment, get_dict_key
from scipy.spatial.distance import cdist
import numpy as np

environment = Environment(3, 5)
state = environment.state
actions = environment.actions


def go_to_coordinate(truck_position, coord, destination):
    if truck_position[1] > coord[1]:
        return actions["go_left"]
    elif truck_position[1] < coord[1]:
        return actions["go_right"]
    else:
        if truck_position[0] > coord[0]:
            return actions["go_up"]
        elif truck_position[0] < coord[0]:
            return actions["go_down"]
        else:
            if destination == "shop1":
                return get_unload_action(state["truck1_inventory"], state["shop1_inventory"])
            elif destination == "shop2":
                return get_unload_action(state["truck1_inventory"], state["shop2_inventory"])
            elif destination == "depot":
                return actions["load_3"]
            else:
                print("ERROR: DESTINATION NOT FOUND")


def mdist(A, B):
    # print(A, B)
    A = A.reshape(1, -1)
    B = B.reshape(1, -1)
    # print("A: {}, B: {}".format(A, B))
    return cdist(A, B, metric='cityblock')[0][0]


def get_unload_action(truck_inventory, shop_inventory):
    max_acceptable_inventory = 3 - shop_inventory
    if truck_inventory < max_acceptable_inventory:
        return actions[get_dict_key(actions, 3 + truck_inventory)]
    else:
        return actions[get_dict_key(actions, 3 + max_acceptable_inventory)]


def benchmark_heuristic(state):
    actions = environment.actions
    # state = environment.state
    truck_position = state["position"]
    depot_position = np.array([0, 2])
    shop1_position = np.array([1, 4])
    shop2_position = np.array([2, 1])

    # Check empty truck
    if state["truck1_inventory"] == 0:
        # Try reducing distance b/w depot and truck
        return go_to_coordinate(truck_position, depot_position, "depot")

    elif state["shop1_inventory"] == 0:
        return go_to_coordinate(truck_position, shop1_position, "shop1")

    elif state["shop2_inventory"] == 0:
        return go_to_coordinate(truck_position, shop2_position, "shop2")

    else:
        if mdist(truck_position, shop1_position) < mdist(truck_position, shop2_position):
            return go_to_coordinate(truck_position, shop1_position, "shop1")

        else:
            return go_to_coordinate(truck_position, shop2_position, "shop2")