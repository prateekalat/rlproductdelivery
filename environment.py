import numpy as np
import sys

class Environment:
    # State of the environment
    state = {
        "position": 1,
        "truck1_inventory": 3,
        "shop1_inventory": 2,
        "shop2_inventory": 3
    }

    # Actions supported by environment
    actions = {
        "go_left": 0,
        "go_right": 1,
        "go_up": 2,
        "go_down": 3,

        "unload_1": 4,
        "unload_2": 5,
        "unload_3": 6,

        "wait": 7
    }

    # Position types are used to decide whether or not certain actions can be performed.
    # Eg. Unload actions can only be performed at shops.
    position_types = {
        "shop": 0,
        "depot": 1,
        "location": 2
    }

    # Each position is mapped to its type
    positions = {
        1: position_types["depot"],
        2: position_types["shop"],
        3: position_types["location"],
        4: position_types["location"],
        5: position_types["shop"]
    }

    # Each position is mapped to a mapping between an action and a position.
    # Eg. 'map[1]["go_left"] = 2' means 'Going left from 1 takes you to 2'
    map = {
        1: {
            actions["go_left"]: 2,
            actions["go_right"]: 4
        },

        2: {
            actions["go_up"]: 1,
            actions["go_right"]: 3,
            actions["go_down"]: 5
        },

        3: {
            actions["go_up"]: 1,
            actions["go_left"]: 2,
            actions["go_right"]: 4,
            actions["go_down"]: 5
        },

        4: {
            actions["go_up"]: 1,
            actions["go_left"]: 3,
            actions["go_down"]: 5
        },

        5: {
            actions["go_up"]: 3,
            actions["go_right"]: 4,
            actions["go_left"]: 2
        }
    }

    def perform_action(self, state, action):
        typeOfLocation = positions[state["position"]]
        typeOfAction = ""
        if(actions[action] <= 3):
            typeOfAction = 'move'
        elif(actions[action] <= 6):
            typeOfAction = 'unload'
        else:
            typeOfAction = 'wait'

        if(typeOfAction == 'move'):
            if(map[state["position"]][action]):
                state["position"] = map[state["position"]][action]
                return getReward(state, action)
            else:
                return -10000

        elif(typeOfAction == 'unload'):
            if(typeOfLocation != 'shop'):
                return -10000
            else:
                if(state["position"] == 2):
                    load = actions[action] - 3
                    state["shop1_inventory"] = max(3, state["shop1_inventory"]+load)
                    return getReward(state, action)
                elif(state["position"] == 5):
                    load = actions[action] - 3
                    state["shop2_inventory"] = max(3, state["shop2_inventory"]+load)
                    return getReward(state, action)
                else:
                    print("Unexpected Error")
                    sys.exit(0)

        else:
            return getReward(state, action)


    def __init__(self):
        pass
