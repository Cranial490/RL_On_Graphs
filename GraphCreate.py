import re
import numpy as np
def create_graph(graphFile):
	states = {}
	volume = {}
	np.random.seed(13)
	with open(graphFile) as f:
		for line in f:
			l =re.sub("[^\d]"," ",line).split()
			if len(l) ==2:
				s1 = int(l[0])
				s2 = int(l[1])
				if s1 not in states:
					states[s1] = []
					states[s1].append(s2)
				else:
					if s2 not in states[s1]:
						states[s1].append(s2)
				if s2 not in states:
					states[s2] = []
		for s in states:
			volume[s] = np.random.randint(50,300)
	return states,volume
