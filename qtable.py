import numpy as np
import random
import matplotlib.pyplot as plt
from environment import Environment
from sim import simrew

if __name__ == "__main__":
    # s=no.of states,a=no.of actions
    s = 960
    a = 11
    # q_table = np.zeros([s, a])
    gamma = 0.95
    # alpha = 0.5
    alp = []
    simreward = []
    benchmarkreward = []
    iterations = 100
    prob_shops = [0.3, 0.2]

    customer_behaviour = np.random.rand(2, iterations)
    customer_behaviour[0] = customer_behaviour[0] < prob_shops[0]
    customer_behaviour[1] = customer_behaviour[1] < prob_shops[1]
    customer_behaviour = customer_behaviour.T.astype(int)

    for q in range(90, 100, 1):
        alpha = q / float(100)
        q_table = np.zeros([s, a])
        epsilon = 0.1
        max_epsilon = 1.0
        min_epsilon = 0.01
        decay_rate = 0.01

        all_epochs = []
        all_penalties = []
        penalties = 0

        environment = Environment(3, 5)

        for i in range(1, 30001):
            # state reset..
            environment.refresh()
            state = environment.state

            epochs, penalties, reward = 0, 0, 0
            done = False
            totalReward = 0
            while not done:
                currStateNumber = environment.getStateNumber()
                if random.uniform(0, 1) < epsilon:
                    action = random.randint(0, a - 1)  # random action
                else:
                    action = np.argmax(q_table[currStateNumber])

                reward = environment.perform_action(action)  # need to return all these ##done,info implement
                totalReward += reward
                newStateNumber = environment.getStateNumber()
                if totalReward <= -100000:  # decide the no.
                    done = True

                next_max = np.max(q_table[newStateNumber])

                q_table[currStateNumber, action] = q_table[currStateNumber, action] + alpha * (
                        reward + gamma * next_max - q_table[currStateNumber, action])

                # if reward == -10:
                #     penalties += 1  # how much to change??

                epochs += 1
            epsilon = min_epsilon + (max_epsilon - min_epsilon) * np.exp(-0.1 * epsilon)
            # if i % 1000 == 0:
            # clear_output(wait=True)
            # print('Episode: {}'.format(i))

        print('Training Finished..')
        np.savetxt("qtable.txt", q_table)
        for i in range(0, len(q_table)):
            # print("position: ", (i//64)%5 +1, "truck1: ", (i//16)%4, "shop1: ", (i//4)%4, "shop2: ", i%4)
            ind = np.argmax(q_table[i])

            actionStr = ""
            for stri, number in environment.actions.items():
                if ind == number:
                    actionStr = stri

        print(q)
        # print(actionStr, max(q_table[i]), "\n")
        sim_reward, heuristic_reward = simrew(customer_behaviour)
        alp.append(alpha)
        simreward.append(sim_reward)
        benchmarkreward.append(heuristic_reward)
        print("SimReward: {}".format(simreward))
        print("BenchReward: {}".format(benchmarkreward))

    plt.plot(alp, simreward, 'r')
    plt.plot(alp, benchmarkreward, 'b')
    plt.xlabel("alpha")
    plt.ylabel("Total Reward")
    plt.show()
