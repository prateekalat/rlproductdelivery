import numpy as np 
import random

#s=no.of states,a=no.of actions
s=320
a=8
q_table= np.zeros([s][a])
gamma=0.9
alpha=0.1

epsilon=0.1
max_epsilon=1.0
min_epsilon=0.01
decay_rate=0.01

all_epochs = []
all_penalities=[]
penalites=0

for i in range(1,100001):
    # state reset..
    state = 0
    
    epochs, penalites,reward = 0,0,0
    done = False

    while not done:
	    currState = state
        if random.uniform(0,1)<epsilon:
            action =  random.randint(0,7)#random action
        else:
            action = np.argmax(q_table[state])
        
        reward = perform_action(state,action) ##need to return all these ##done,info implement
        if reward <= -1000 #decide the no.
        	done = True
        
        next_max = np.max(q_table[state])
        
        q_table[currState,action] =  q_table[currState,action] + alpha * ( reward + gamma * next_max - q_table[currState,action])
       
        
        if reward == -10:
            penalities +=1		#how much to change??
        
        
        epochs +=1
    epsilon= min_epsilon +(max_epsilon-min_epsilon) * np.exp(-0.1*epsilon)
    if i%100==0:
        clear_output(wait=True)
        print('Episode: {}'.format(i))

print('Training Finished..')