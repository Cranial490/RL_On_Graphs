import numpy as np
from GraphCreate import create_graph
#-----------------------------------------------------------------------------
hop_limit = 3
#hop_count = 0
episodes = 10000
start_state = 0
epsilon = 0.3
alpha = 0.1
gamma = 0.8
terminate = -1
np.random.seed(13)
#-------------------------------Graph Creation---------------------------------
state_action,volume = create_graph("dummy.txt")
def get_reward(graph,volume,frm,to):
	if to in state_action[frm]:      
		return volume[to]-volume[frm]
	else:
		return None
def get_actions(graph,state):
	return state_action[state]
# selects the action with max Q value
def max_Q(Q_matrix,s):
	return max(Q_matrix[s].keys(), key=(lambda k: Q_matrix[s][k]))
# selects action based on epsilon greedy policy
def select_action(graph,curr_state,Q,epsilon):
	A = get_actions(graph,curr_state)
	#print curr_state,A
	if len(A)==0:
		#print "terminate"
		return -1 # terminal
	p = np.random.random()
	if p < (1-epsilon):
		#print "greedy"
		return max_Q(Q,curr_state)
	else:
		#print "random"
		return np.random.choice(A)
def select_action_greedy(graph,curr_state,Q_matrix):
	A = get_actions(graph,curr_state)
	if len(A)==0:
		return -1
	else:
		return max_Q(Q_matrix,curr_state)
#-----------------------------------------------------------------------------
#-----------------------SARSA implementation----------------------------------

#Creating and initializing the Q matrix
Q = {}
states = state_action.keys()
for s in states:
	Q[s] = {}
	for a in get_actions(state_action,s):
		Q[s][a] = 0

for i in range(episodes):
	error = 0
	hop_count = 0
	curr_state = 0
	action = select_action(state_action,curr_state,Q,epsilon)
	if action == terminate:
		print "start state cannot be terminal"
		break
	#episode starts
	while hop_count <= hop_limit:
		reward = get_reward(state_action,volume,curr_state,action)
		s_dash = action
		#print "s' is ",s_dash
		a_dash = select_action(state_action,s_dash,Q,epsilon)
		#print "current state",curr_state," action",action," reward",reward
		if a_dash == terminate:
			#print "terminating"
			break
		else:
			hop_count = hop_count + 1
			old_Q = Q[curr_state][action]
			Q[curr_state][action] = Q[curr_state][action] + alpha*(reward + gamma*Q[s_dash][a_dash] - Q[curr_state][action])
			#calculate error
			error = max(error,abs(Q[curr_state][action]-old_Q))
			#print "updated..",Q[curr_state][action]
			curr_state = s_dash
			action = a_dash
		print "diff: ",error
print Q

#---------------------------------------------------------------------------------------
#--------------------------Greedy control-----------------------------------------------
def greedy_control(graph,start_state,Q_matrix):
	path = []
	s = start_state
	action = select_action_greedy(graph,s,Q_matrix)
	while (action!=terminate and hop_count <= hop_limit):
		path.append(s)
		s = action
		action = select_action_greedy(graph,s,Q_matrix)
	return path
print "optimal path from state: ",start_state
print greedy_control(state_action,start_state,Q)










