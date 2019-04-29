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
        if position[1] != 0:
            position[1] -= 1
            reward = -0.1
        else:
            reward = -1000
    if action == "go_right":
        if position[1] != m - 1:
            position[1] += 1
            reward = -0.1
        else:
            reward = -1000
    if action == "go_up":
        if position[0] != 0:
            position[0] -= 1
            reward = -0.1
        else:
            reward = -1000
    if action == "go_down":
        if position[0] != n - 1:
            position[0] += 1
            reward = -0.1
        else:
            reward = -1000
    return position, reward


class Environment:
    # State of the environment

    # Actions supported by environment

    prob_shops = [0.3, 0.2]
    # prob_shops = [0, 0]

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
        "unload": 50,
        "load": 5
    }

    def perform_action(self, truck_id, action, customer_behavior=None):
        action = get_dict_key(self.actions, action)

        reward = 0

        # shops = ["shop1_inventory", "shop2_inventory"]
        for index, value in enumerate(self.state["shop_inventory"]):
            if customer_behavior is None:
                n = random.random()
                n = n <= self.prob_shops[index]
            else:
                n = customer_behavior[index]
            if n != 0:
                inventory = value
                if inventory > 0:
                    self.state["shop_inventory"][index] -= 1
                else:
                    reward += self.rewards["empty"]

        position = self.state["position"][truck_id]
        positionInd = position[0] * 5 + position[1]

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
            position = self.state["position"][truck_id]
            newPosition, r = moveTruck(position, action, self.n, self.m)  # TODO change moveTruck to account for multi-truck
            if r == -1000:
                return -1000  # TODO Might be causing high negative reward *FIX*
            else:
                self.state["position"][truck_id] = newPosition

        elif type_of_action == 'unload':
            if type_of_location != self.position_types["shop"]:
                return -10000
            else:
                if (self.state["position"][truck_id] == [1, 4]).all():
                    L = self.actions[action] - 3
                    T = self.state["truck_inventory"][truck_id]
                    S = self.state["shop_inventory"][0]

                    T = T - L
                    S = S + L
                    if T < 0 or S > 3:
                        return -10000
                    self.state["shop_inventory"][0] = S
                    self.state["truck_inventory"][truck_id] = T
                    reward += self.rewards["unload"]
                elif (self.state["position"][truck_id] == [2, 1]).all():
                    L = self.actions[action] - 3
                    T = self.state["truck_inventory"][truck_id]
                    S = self.state["shop_inventory"][1]

                    T = T - L
                    S = S + L
                    if T < 0 or S > 3:
                        return -10000
                    self.state["shop_inventory"][1] = S
                    self.state["truck_inventory"][truck_id] = T
                    reward += self.rewards["unload"]
                else:
                    print("Unexpected Error")
                    sys.exit(0)

        elif type_of_action == 'load':
            if type_of_location != self.position_types["depot"]:
                return -10000
            else:
                L = self.actions[action] - 6
                T = self.state["truck_inventory"][truck_id]

                T = T + L
                if T > 3:
                    return -10000
                self.state["truck_inventory"][truck_id] = T
                reward += self.rewards["load"]
        return reward

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.state = {
            "position": np.array([[0, 0], [2, 3]]),
            "truck_inventory": np.array([3, 3]),
            "shop_inventory": np.array([2, 3])
        }

    def refresh(self):
        self.state['position'] = np.array([[0, 0], [2, 3]])
        self.state["truck_inventory"] = np.array([3, 3])
        self.state["shop_inventory"] = np.array([2, 3])

    def getStateNumber(self):
        state = self.state
        positionArray = np.array([i[0] * 5 + i[1] for i in state["position"]])  # Each element b/w 0-14
        shopStateNumber = state["shop_inventory"][0] * 4 + state["shop_inventory"][1]  # Number b/w 0-15
        truckInventoryState = state["truck_inventory"][0] * 4 + state["truck_inventory"][1]  # Number b/w 0-15
        positionStateNumber = positionArray[0] * 15 + positionArray[1]  # 0 - 224
        return (16 ** 2) * positionStateNumber + 16 * shopStateNumber + truckInventoryState  # 0 - 57599
