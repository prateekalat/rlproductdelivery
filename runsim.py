import os

directory = './reward_test'

for filename in os.listdir(directory):
	if filename.endswith(".txt"): 
		leftList = [i for i, x in enumerate(filename) if x=="("]
		rightList = [i for i, x in enumerate(filename) if x==")"]
		args = [filename[leftList[i]+1:rightList[i]] for i in range(len(leftList))]

		reward = 0
		for i in range(3):
			log = os.popen("python3 sim.py " + str(args[0]) + " " + str(args[1]) + " " + str(args[2])).read()
			log = log.split("\n")
			reward += int(log[-2])
		print(reward/3, args)
