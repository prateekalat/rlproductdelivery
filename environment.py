import numpy as np
import sys
import random


def get_dict_key(dictionary, value):
    final_key = None
    for key, dict_val in dictionary.items():
        if value == dict_val:
            final_key = key
    return final_key

def moveTruck(position, action, n, m):
    reward = 0
    if action == "go_left":
        if(position[1] != 0):
            position[1] -= 1
            reward = -0.1
        else:
            reward = -1000
    if action == "go_right":
        if(position[1] != m-1):
            position[1] += 1
            reward = -0.1
        else:
            reward = -1000
    if action == "go_up":
        if(position[0] != 0):
            position[0] -= 1
            reward = -0.1
        else:
            reward = -1000
    if action == "go_down":
        if(position[0] != n-1):
            position[0] += 1
            reward = -0.1
        else:
            reward = -1000
    return position, reward


class Environment:
    # State of the environment
    state = {
        "position": np.array([0, 0]),
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

    # shopArray = [9, 11]
    # shopArray = [[1, 4], [2, 1]]
    # depotArray = [2]
    # depotArray = [[0, 2]]

    # Each position is mapped to its type
    positions = {
        0: position_types["location"],
        1: position_types["location"],
        2: position_types["depot"],
        3: position_types["location"],
        4: position_types["location"],
        5: position_types["location"],
        6: position_types["location"],
        7: position_types["location"],
        8: position_types["location"],
        9: position_types["shop"],
        10: position_types["location"],
        11: position_types["shop"],
        12: position_types["location"],
        13: position_types["location"],
        14: position_types["location"],
    }

    rewards = {
        "fuel": -0.1,
        "empty": -5,
        "unload": 10,
        "load": 5
    }

    def perform_action(self, action):
        action = get_dict_key(self.actions, action)

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

        position = self.state["position"]
        positionInd = position[0]*5 + position[1]

        type_of_location = self.positions[positionInd]
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
            position = self.state["position"]
            newPosition, r = moveTruck(position, action, self.n, self.m)
            if(r == -1000):
                return -1000
            else:
                self.state["position"] = newPosition

            # if self.actions[action] in self.map[self.state["position"]]:
            #     # print(1)
            #     self.state["position"] = self.map[self.state["position"]][self.actions[action]]
            # else:
            #     return -10000

        elif type_of_action == 'unload':
            if type_of_location != self.position_types["shop"]:
                return -10000
            else:
                if self.state["position"] == [1, 4]:
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
                elif self.state["position"] == [2, 1]:
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

    def __init__(self, n, m):
        self.n = n
        self.m = m

    def refresh(self):
        self.state = {
            "position": [0, 0],
            "truck1_inventory": 3,
            "shop1_inventory": 2,
            "shop2_inventory": 3
        }

    def getStateNumber(self):
        state = self.state
        position = state["position"]
        positionInd = position[0]*5 + position[1]
        # print(state["position"], positionInd)
        return ((4 ** 3) * (positionInd) + (4 ** 2) * (state["truck1_inventory"]) + (4 ** 1) * (
            state["shop1_inventory"]) + state["shop2_inventory"])


