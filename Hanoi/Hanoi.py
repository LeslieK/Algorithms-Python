# Given a start state and a goal state, find the shortest path from start to goal
from collections import defaultdict, deque
from GraphLib import Graph
from BreadthFirstSearch import BreadthFirstSearch as BFS

# read input
# N = number of discs, K = number of pegs
N, _, K = raw_input('N K: ')
num_discs = int(N)
num_pegs = int(K)

initial = raw_input('initial: ')
final = raw_input('final: ')

# initial = [1, 1]
initial = [int(i) for i in initial.split()]
# final = [2, 2]
final = [int(i) for i in final.split()]

# dictionary: curr_state => [ (next_state, action), (next_state, action), ... ]
d = defaultdict(list)
# map state to vertex
symTbl = {}
# map vertex to state
symTbl2 = {}

# put disc on peg j: q[disc] = j
# pop disc from peg: q[disc] = -1

def next_state(curr_state):
	"Finds all successor states from curr_state and adds results to dictionary"
	# marked[0] = 0 is a dummy position so indexing can begin at 1
	
	for disc in range(1, num_discs+1):
		# reset state before moving each disc
		# 0 is inserted into q so indexing can begin at 1
		q = [0]
		q.extend(curr_state[:])
		# action = ()
		# key = (tuple(curr_state), action)
		key = tuple(curr_state)
		# set up marked so all pegs left of disc are marked
		marked = build_marked(q, disc)

		# remove disc from peg
		from_peg = q[disc]
		if not marked[from_peg]:
			q[disc] = -1
			marked[from_peg] = True
			for to_peg in range(1, num_pegs+1):
				# try putting this disc on different pegs
				if not marked[to_peg]:
					# put disc on peg
					q[disc] = to_peg 
					marked[to_peg] = True
					action = (from_peg, to_peg)
					# store next_state
					ns = tuple(q[1:])
					item = (ns, action)
					if item not in d[key]:
						d[key].append(item)
	# return list of successor states: [ (next_state, action), (next_state, action), ... ]
	return d[key]

def build_marked(q, disc):
	# set up marked
	marked = [False for i in range(0, num_pegs+1)]
	for i in range(1, disc):
		pegonleft = q[i]
		marked[pegonleft] = True
	return marked

def buildDictOfStates(initial):
	q = deque()
	q.append(initial)
	marked = [initial]
	while len(q) > 0:
		state = q.popleft()
		nextStates = next_state(state)
		for e in nextStates:
			# (next_state, action)
			ns = e[0]
			if ns not in marked:
				marked.append(ns)
				q.append(ns)

def buildSymTbls():
	"""
	map state to integer vertex
	map vertex to state
	"""
	i = 0
	for key in d.keys():
		# map state to vertex
		symTbl[key] = i
		# map vertex to state
		symTbl2[i] = key
		i += 1

def buildGraph():
	"build graph from state transitions"
	G = Graph(len(d))

	for e in d.iteritems():
		# e = (  key, [ (next_state, action), ..., (next_state, action) ]  )
		v = symTbl[e[0]]
		for s in e[1]:
			ns = s[0]
			action = s[1]
			w = symTbl[ns]
			G.addEdge(v, w)
	return G

def buildActions(path):
	actions = []
	for i in range(len(path)-1):
		from_state = path[i]
		to_state = path[i+1]
		# convert from integer to form [1, 1]
		from_state = symTbl2[from_state]
		to_state = symTbl2[to_state]
		for e in d[from_state]:
			if e[0] == to_state:
				actions.append(e[1])
	return actions

def solution(initial):
	buildDictOfStates(initial)
	buildSymTbls()
	G = buildGraph()
	source = symTbl[tuple(initial)]
	node = symTbl[tuple(final)]
	abfs = BFS(G, source)
	# path is represented as a list of vertices
	path = abfs.pathTo(node)
	if path is None: return "No solution"
	# actions = [ (1, 2), (2, 3) ]
	actions = buildActions(path)
	dist = abfs.distTo(node)
	print dist
	for action in actions:
		print '{0} {1}'.format(action[0], action[1])
	return dist, actions

buildDictOfStates(initial)
buildSymTbls()
G = buildGraph()
source = symTbl[tuple(initial)]
node = symTbl[tuple(final)]
abfs = BFS(G, source)
# path is represented as a list of vertices
path = abfs.pathTo(node)
if path is None: print "No solution"
# actions = [ (1, 2), (2, 3) ]
actions = buildActions(path)
dist = abfs.distTo(node)
print dist
for action in actions:
	print '{0} {1}'.format(action[0], action[1])