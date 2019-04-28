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
    prob_shops = [0.1, 0.5]
    customer_behaviour = np.random.rand(2, iterations)
    customer_behaviour[0] = customer_behaviour[0] < prob_shops[0]
    customer_behaviour[1] = customer_behaviour[1] < prob_shops[1]
    customer_behaviour = customer_behaviour.T.astype(int)

    print(customer_behaviour[:10])
    for i in range(iterations):
        # continue
        print(s0)
        stateNumber = environment.getStateNumber()
        action = np.argmax(q_table[stateNumber])
        # print(stateNumber, q_table[stateNumber])

        actionStr = ""
        for stri, number in environment.actions.items():
            if action == number:
                actionStr = stri

        action = actionStr

        print("Behavior: {}".format(customer_behaviour[i]))
        reward = environment.perform_action(environment.actions[action], customer_behaviour[i])
        totalReward1 += reward
        s0 = environment.state

    # print(action, totalReward1, "\n")
    environment = Environment(3, 5)
    s0 = environment.state
    print(customer_behaviour[:3])
    print("---STARTING HEURISTIC--")
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
        # print("Behavior: {}".format(customer_behaviour[i]))
        reward = environment.perform_action(environment.actions[action], customer_behaviour[i])
        totalReward2 += reward
        s0 = environment.state
    return totalReward1, totalReward2


if __name__ == "__main__":
    print(simrew())
