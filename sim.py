import numpy as np

from benchmark import BenchmarkHeuristic
from environment import Environment


def simrew(customer_behaviour):
    environment = Environment(3, 5)
    q_table = np.loadtxt("qtable.txt")

    s0 = environment.state

    totalReward1 = 0
    totalReward2 = 0
    # while(totalReward >= -1000 and totalReward <= 1000):
    iterations = 100
    prob_shops = environment.prob_shops
    # customer_behaviour = np.random.rand(2, iterations)
    # customer_behaviour[0] = customer_behaviour[0] < prob_shops[0]
    # customer_behaviour[1] = customer_behaviour[1] < prob_shops[1]
    # customer_behaviour = customer_behaviour.T.astype(int)

    for i in range(iterations):
        # continue
        print(s0)
        stateNumber = environment.getStateNumber()
        action = np.argmax(q_table[stateNumber])

        actionStr = ""
        for stri, number in environment.actions.items():
            if action == number:
                actionStr = stri


        action = actionStr
        print(action)

        reward = environment.perform_action(environment.actions[action], customer_behaviour[i])  # todo Add truck_id
        totalReward1 += reward
        s0 = environment.state

    environment = Environment(3, 5)
    s0 = environment.state
    print("---STARTING HEURISTIC--")
    for i in range(iterations):
        print(s0)
        stateNumber = environment.getStateNumber()
        benchmark = BenchmarkHeuristic(environment)
        action = benchmark.benchmark_heuristic()

        actionStr = ""
        for stri, number in environment.actions.items():
            if action == number:
                actionStr = stri

        action = actionStr
        print(action)
        reward = environment.perform_action(environment.actions[action], customer_behaviour[i])  # TODO Add truck_id
        totalReward2 += reward
        s0 = environment.state
    print(totalReward2)
    return totalReward1, totalReward2


if __name__ == "__main__":
    print(simrew())
