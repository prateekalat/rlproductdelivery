from environment import Environment
import numpy as np

environment = Environment()
q_table = np.loadtxt("qtable.txt")

s0 = environment.state

totalReward = 0
# while(totalReward >= -1000 and totalReward <= 1000):
iterations = 100
for i in range(iterations):
	print(s0)
	stateNumber = (4**3)*(s0["position"]-1) + (4**2)*(s0["truck1_inventory"]) + (4**1)*(s0["shop1_inventory"]) + s0["shop2_inventory"]
	action = np.argmax(q_table[stateNumber])
	print(stateNumber, q_table[stateNumber])

	actionStr = ""
	for stri, number in environment.actions.items():
		if action == number:
			actionStr =  stri

	action = actionStr

	reward = environment.perform_action(environment.actions[action])
	totalReward+=reward
	s0 = environment.state

	# print(action, totalReward, "\n")
