import numpy as np

from benchmark import BenchmarkHeuristic
from environment import Environment
import copy

import sys


def simrew():
    N = 6; M = 10; T = 1; S = 4; I_T = 4; I_S = 4

    env = []

    rewards = {
        "fuel": int(sys.argv[1]),
        "empty": int(sys.argv[2]),
        "unload": int(sys.argv[3]),
        "load": int(sys.argv[3]),
        "wall": int(sys.argv[1]),
        "illegal": -100
    }

    q_table = np.loadtxt("./reward_test/qtable("+str(sys.argv[1])+")("+str(sys.argv[2])+")("+str(sys.argv[3])+").txt")

    for i in range(T):
        env.append(Environment(N, M, T, S, I_T, I_S, rewards))

    env[0].state["position"] = [[5, 9]]

    totalReward = 0
    iterations = 200

    for i in range(iterations):
        for t in range(T):
            stateNumber = env[t].getStateNumber()
            action = np.argmax(q_table[stateNumber])

            actionStr = ""
            for stri, number in env[t].actions.items():
                if action == number:
                    actionStr = stri

            action = actionStr

            reward = env[t].perform_action(0, env[t].actions[action])
            totalReward += reward
            print(reward, action)

            # for t2 in range(T):
            #     env[t2].state["shop_inventory"] = env[t].state["shop_inventory"]
        
        print(env[0].state)
        # print("-----------------------")
        # print(env[1].state)
        print("\n")

    return totalReward


if __name__ == "__main__":
    totalReward = simrew()
    print(totalReward)

