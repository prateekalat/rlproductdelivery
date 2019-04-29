import numpy as np
import random
import matplotlib.pyplot as plt
from environment import Environment
from sim import simrew


if __name__ == "__main__":
    # s=no.of states,a=no.of actions
    s = 57600
    a = 11 ** 2
    # q_table = np.zeros([s, a])
    gamma = 0.95
    alpha = 0.8
    alp = []
    simreward = []
    benchmarkreward = []
    iterations = 100
    prob_shops = [0.3, 0.2]

    customer_behaviour = np.random.rand(2, iterations)
    customer_behaviour[0] = customer_behaviour[0] < prob_shops[0]
    customer_behaviour[1] = customer_behaviour[1] < prob_shops[1]
    customer_behaviour = customer_behaviour.T.astype(int)

    for q in range(99, 100, 1):
        # alpha = q / float(100)
        q_table = np.zeros([s, a])
        epsilon = 0.1
        max_epsilon = 1.0
        min_epsilon = 0.01
        decay_rate = 0.01

        all_epochs = []
        all_penalties = []
        penalties = 0

        environment = Environment(3, 5)

        for i in range(1, 300001):
            # state reset..
            environment.refresh()
            state = environment.state

            epochs, penalties, reward = 0, 0, 0
            done = False
            totalReward = 0
            while not done:
                action_array = np.array([0, 0], dtype=int)
                currStateNumber = environment.getStateNumber()
                for truck_id in range(len(state["position"])):
                    if random.uniform(0, 1) < epsilon:
                        action_array[truck_id] = np.random.randint(11)  # random action
                    else:
                        if truck_id == 0:
                            action_array[truck_id] = np.argmax(q_table[currStateNumber]) // 11
                        elif truck_id == 1:
                            action_array[truck_id] = np.argmax(q_table[currStateNumber]) % 11

                for truck_id in range(len(state["position"])):
                    reward += environment.perform_action(truck_id, action_array[truck_id])
                totalReward += reward
                newStateNumber = environment.getStateNumber()
                # print(totalReward) #totalReward min value = -1000 * ??
                if totalReward <= -10000 or totalReward >= 1000:  # decide the no.
                    done = True
                    # sys.exit(0)

                next_max = np.max(q_table[newStateNumber])

                action = action_array[0]*11 + action_array[1]

                q_table[currStateNumber, action] = q_table[currStateNumber, action] + alpha * (
                        reward + gamma * next_max - q_table[currStateNumber, action])
                epochs += 1
            epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-0.1 * epsilon)
            if i % 10000 == 0:
                print('Episode: {}'.format(i))
                environment.refresh()

                for j in range(100):
                    s0 = environment.state
                    print("State:{}".format(s0))
                    print()
                    sNumber = environment.getStateNumber()
                    actionNum = np.argmax(q_table[sNumber])
                    reward = [0, 0]
                    action_array= [actionNum//11, actionNum%11]

                    for truck_id in range(2):
                        if truck_id == 0:
                            reward[truck_id] = environment.perform_action(truck_id, actionNum//11)
                        elif truck_id == 1:
                            reward[truck_id] = environment.perform_action(truck_id, actionNum%11)
                    actionStr_array = ["", ""]
                    for j in range(2):
                        actionStr = ""
                        for stri, number in environment.actions.items():
                            if action_array[j] == number:
                                actionStr = stri
                        actionStr_array[j] = actionStr
                    print("Action:{}".format(actionStr_array))
                    print()
                    print("NewState: {}".format(s0))
                    print()
                    print("Reward:{}".format(reward))
                    print()



        print('Training Finished..')
        np.savetxt("qtable.txt", q_table)
        actionStr_array = ["", ""]
        
        # print(q)
        # sim_reward, heuristic_reward = simrew(customer_behaviour)
        # alp.append(alpha)
        # simreward.append(sim_reward)
        # benchmarkreward.append(heuristic_reward)
        # print("SimReward: {}".format(simreward))
        # print("BenchReward: {}".format(benchmarkreward))

    # plt.plot(alp, simreward, 'r')
    # plt.plot(alp, benchmarkreward, 'b')
    # plt.xlabel("alpha")
    # plt.ylabel("Total Reward")
    # plt.show()
