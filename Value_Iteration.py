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
# selects the next state with max value for a state s.
def max_V(graph,V_matrix,s):
	act = graph[s]
	return max(act, key=(lambda k: V_matrix[k]))
# selects action based on epsilon greedy policy
def select_action(graph,curr_state,V,epsilon):
	A = get_actions(graph,curr_state)
	#print curr_state,A
	if len(A)==0:
		#print "terminate"
		return -1 # terminal
	p = np.random.random()
	if p < (1-epsilon):
		#print "greedy"
		return max_V(graph,V,curr_state)
	else:
		#print "random"
		return np.random.choice(A)
def select_action_greedy(graph,curr_state,V_matrix):
	A = get_actions(graph,curr_state)
	print A
	if len(A)==0:
		return -1
	else:
		return max_V(graph,V_matrix,curr_state)
#-----------------------------------------------------------------------------
#-----------------------Value_Iteration implementation----------------------------------

#Creating and initializing the Q matrix
V = {}
states = state_action.keys()
for s in states:
	V[s] = 0

for i in range(episodes):
	error = 0
	hop_count = 0
	curr_state = 0
	action = select_action(state_action,curr_state,V,epsilon)
	if action == terminate:
		#V[curr_state] = 0
		print "start state cannot be terminal"
		break
	#episode starts
	while hop_count <= hop_limit:
		action = select_action(state_action,curr_state,V,epsilon)
		reward = get_reward(state_action,volume,curr_state,action)
		if reward == None:
			#teminate episode
			break
		s_dash = action
		#print "s' is ",s_dash
		#print "current state",curr_state,"reward",reward
		hop_count = hop_count + 1
		old_V = V[curr_state]
		V[curr_state] = V[curr_state] + alpha*(reward + gamma*V[s_dash] - V[curr_state])
		#calculate error
		error = max(error,abs(V[curr_state]-old_V))
		#print "updated..",Q[curr_state][action]
		curr_state = s_dash
		#print "diff: ",error
print V

#---------------------------------------------------------------------------------------
#--------------------------Greedy control-----------------------------------------------
def greedy_policy(graph,start_state,V_matrix):
	path = []
	s = start_state
	hop_count =0
	visited = []
	action = select_action_greedy(graph,s,V_matrix)
	while (action!=terminate and hop_count <= hop_limit):
		s = action
		hop_count = hop_count + 1
		visited.append(s)
		path.append(s)
		action = select_action_greedy(graph,s,V_matrix)
	return path
print "optimal path from state: ",start_state
print greedy_policy(state_action,start_state,V)









