import numpy as np
import sys
import random


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

    def get_reward(self, state, action):

        purchase_probability = 0.05
        iterations = 0

        reward = -0.1
        shops = ["shop1_inventory", "shop2_inventory"]
        prob_shops = [0.1, 0.5]
        for i in range(0, len(shops)):
            n = random.random()
            if n <= prob_shops[i]:
                inventory = self.state[shops[i]]
                if inventory > 0:
                    self.state[shops[i]] -= 1

        L = self.actions[action] - 3
        T = state["truck1_inventory"]
        if state["position"] == 2:
            S = state["shop1_inventory"]
        elif state["position"] == 5:
            S = state["shop2_inventory"]
        else:
            print("Unexpected Error")
            sys.exit(0)

        T = T - L
        S = S + L
        if T < 0 or S > 3:
            return -10000

        reward += 10 ** (S - 3)

        return reward

    def perform_action(self, state, action):
        type_of_location = self.positions[state["position"]]
        type_of_action = ""
        if self.actions[action] <= 3:
            type_of_action = 'move'
        elif self.actions[action] <= 6:
            type_of_action = 'unload'
        else:
            type_of_action = 'wait'

        if type_of_action == 'move':
            if self.map[state["position"]][action]:
                state["position"] = self.map[state["position"]][action]
                return self.get_reward(state, action)
            else:
                return -10000

        elif type_of_action == 'unload':
            if type_of_location != 'shop':
                return -10000
            else:
                if state["position"] == 2:
                    load = self.actions[action] - 3
                    state["shop1_inventory"] = max(3, state["shop1_inventory"] + load)
                    return self.get_reward(state, action)
                elif state["position"] == 5:
                    load = self.actions[action] - 3
                    state["shop2_inventory"] = max(3, state["shop2_inventory"] + load)
                    return self.get_reward(state, action)
                else:
                    print("Unexpected Error")
                    sys.exit(0)

        else:
            return self.get_reward(state, action)

    def __init__(self):
        pass
