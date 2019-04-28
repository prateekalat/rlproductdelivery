from environment import Environment, get_dict_key
from scipy.spatial.distance import cdist
import numpy as np

environment = Environment(3,5)
actions = environment.actions

def mdist(A, B):
    # print(A, B)
    A = A.reshape(1, -1)
    B = B.reshape(1, -1)
    return cdist(A, B, metric='cityblock')


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
    depot_position = np.array([0, 1])
    shop1_position = np.array([1, 2])
    shop2_position = np.array([6, 5])


    # Check empty truck
    if state["truck1_inventory"] == 0:
        # Try reducing distance b/w depot and truck
        if truck_position[0] > depot_position[0]:
            return actions["go_left"]
        elif truck_position[0] < depot_position[0]:
            return actions["go_right"]
        elif truck_position[1] > depot_position[1]:
            return actions["go_up"]
        elif truck_position[1] < depot_position[1]:
            return actions["go_down"]
        else:
            return actions["load_3"]
    elif state["shop1_inventory"] == 0:
        if truck_position[0] > shop1_position[0]:
            return actions["go_left"]
        elif truck_position[0] < shop1_position[0]:
            return actions["go_right"]
        elif truck_position[1] > shop1_position[1]:
            return actions["go_up"]
        elif truck_position[1] < shop1_position[1]:
            return actions["go_down"]
        else:
            return actions["unload_3"]

    elif state["shop2_inventory"] == 0:
        if truck_position[0] > shop2_position[0]:
            return actions["go_left"]
        elif truck_position[0] < shop2_position[0]:
            return actions["go_right"]
        elif truck_position[1] > shop2_position[1]:
            return actions["go_up"]
        elif truck_position[1] < shop2_position[1]:
            return actions["go_down"]
        else:
            return actions["unload_3"]
    else:
        if mdist(truck_position, shop1_position) < mdist(truck_position, shop2_position):
            if truck_position[0] > shop1_position[0]:
                return actions["go_left"]
            elif truck_position[0] < shop1_position[0]:
                return actions["go_right"]
            elif truck_position[1] > shop1_position[1]:
                return actions["go_up"]
            elif truck_position[1] < shop1_position[1]:
                return actions["go_down"]
            else:
                return actions["unload_3"]
        else:
            if truck_position[0] > shop2_position[0]:
                return actions["go_left"]
            elif truck_position[0] < shop2_position[0]:
                return actions["go_right"]
            elif truck_position[1] > shop2_position[1]:
                return actions["go_up"]
            elif truck_position[1] < shop2_position[1]:
                return actions["go_down"]
            else:
                return actions["unload_3"]
