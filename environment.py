import numpy as np


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

    def perform_action(self, agent, action):
        pass

    def __init__(self):
        pass
