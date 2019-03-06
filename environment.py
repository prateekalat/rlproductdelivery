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

        "load_1": 7,
        "load_2": 8,
        "load_3": 9,

        "wait": 10
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

    rewards = {
        "fuel": -0.1,
        "empty": -5,
        "unload": 10,
        "load": 5
    }

    def perform_action(self, action):
        actionStr = ""
        for stri, number in self.actions.items():
            if action == number:
                actionStr = stri

        action = actionStr

        reward = 0

        shops = ["shop1_inventory", "shop2_inventory"]
        prob_shops = [0.1, 0.5]
        for i in range(0, len(shops)):
            n = random.random()
            if n <= prob_shops[i]:
                inventory = self.state[shops[i]]
                if inventory > 0:
                    self.state[shops[i]] -= 1
                else:
                    reward += self.rewards["empty"]

        type_of_location = self.positions[self.state["position"]]
        type_of_action = ""

        if self.actions[action] <= 3:
            type_of_action = 'move'
        elif self.actions[action] <= 6:
            type_of_action = 'unload'
        elif self.actions[action] <= 9:
            type_of_action = 'load'
        else:
            type_of_action = 'wait'

        if type_of_action == 'move':
            reward += self.rewards["fuel"]
            if self.actions[action] in self.map[self.state["position"]]:
                # print(1)
                self.state["position"] = self.map[self.state["position"]][self.actions[action]]
            else:
                return -10000

        elif type_of_action == 'unload':
            if type_of_location != self.position_types["shop"]:
                return -10000
            else:
                if self.state["position"] == 2:
                    L = self.actions[action] - 3
                    T = self.state["truck1_inventory"]
                    S = self.state["shop1_inventory"]

                    T = T - L
                    S = S + L
                    if T < 0 or S > 3:
                        return -10000
                    self.state["shop1_inventory"] = S
                    self.state["truck1_inventory"] = T
                    reward += self.rewards["unload"]
                elif self.state["position"] == 5:
                    L = self.actions[action] - 3
                    T = self.state["truck1_inventory"]
                    S = self.state["shop2_inventory"]

                    T = T - L
                    S = S + L
                    if T < 0 or S > 3:
                        return -10000
                    self.state["shop2_inventory"] = S
                    self.state["truck1_inventory"] = T
                    reward += self.rewards["unload"]
                else:
                    print("Unexpected Error")
                    sys.exit(0)

        elif type_of_action == 'load':
            if type_of_location != self.position_types["depot"]:
                return -10000
            else:
                L = self.actions[action] - 6
                T = self.state["truck1_inventory"]

                T = T + L
                if T > 3:
                    return -10000
                self.state["truck1_inventory"] = T
                reward += self.rewards["load"]
        return reward

    def __init__(self):
        pass

    def refresh(self):
        self.state = {
            "position": 1,
            "truck1_inventory": 3,
            "shop1_inventory": 2,
            "shop2_inventory": 3
        }

    def getStateNumber(self):
        state = self.state
        return ((4 ** 3) * (state["position"] - 1) + (4 ** 2) * (state["truck1_inventory"]) + (4 ** 1) * (
        state["shop1_inventory"]) + state["shop2_inventory"])
