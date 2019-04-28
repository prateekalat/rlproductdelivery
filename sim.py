import numpy as np

from benchmark import benchmark_heuristic
from environment import Environment


def simrew():
    environment = Environment(3, 5)
    q_table = np.loadtxt("qtable.txt")

    s0 = environment.state

    totalReward1 = 0
    totalReward2 = 0
    # while(totalReward >= -1000 and totalReward <= 1000):
    iterations = 100
    for i in range(iterations):
        # continue
        print(s0)
        stateNumber = environment.getStateNumber()
        # stateNumber = (4**3)*(s0["position"]-1) + (4**2)*(s0["truck1_inventory"]) + (4**1)*(s0["shop1_inventory"]) + s0["shop2_inventory"]
        action = np.argmax(q_table[stateNumber])
        # print(stateNumber, q_table[stateNumber])

        actionStr = ""
        for stri, number in environment.actions.items():
            if action == number:
                actionStr = stri

        action = actionStr

        reward = environment.perform_action(environment.actions[action])
        totalReward1 += reward
        s0 = environment.state

    # print(action, totalReward1, "\n")
    environment = Environment(3, 5)
    s0 = environment.state
    for i in range(iterations):
        print(s0)
        stateNumber = environment.getStateNumber()
        action = benchmark_heuristic(s0)
        # print(stateNumber, q_table[stateNumber])

        actionStr = ""
        for stri, number in environment.actions.items():
            if action == number:
                actionStr = stri

        action = actionStr
        print(action)
        reward = environment.perform_action(environment.actions[action])
        totalReward2 += reward
        s0 = environment.state
    return totalReward1, totalReward2


if __name__ == "__main__":
    print(simrew())
