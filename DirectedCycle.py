# detect a directed cycle in a connected digraph using DFS
#
# DG = Digraph(13)
# DG.addEdge(v, w)
# ...
# dc = DirectedCycle(DG)
# dc.cycle()
# returns: 2 0 5 4 2


class DC(object):
	"finds first directed cycle in a digraph"
	def __init__(self, G):
		self._marked = [False for _ in range(G.V())]
		self._edgeTo = [-1 for _ in range(G.V())]
		self._onStack = [False for _ in range(G.V())]
		self._cycle = []
		self._cycleFound = False
		for v in range(G.V()):
			if self._cycleFound: return
			if not self._marked[v]:
				self._dfs(G, v)

	def _dfs(self, G, v):
		if self._cycleFound: return
		else:
			self._marked[v] = True
			self._onStack[v] = True
			for w in G.adj(v):
				"vertices downstream and adjacent to v are in adj[v]"
				if not self._marked[w]:
					self._edgeTo[w] = v
					#print 'entering dfs', 'v = ', v, 'w = ', w
					self._dfs(G, w)
				elif self._onStack[w]:
					# found cycle
					if not self._cycleFound: 
						self._cycleFound = True
						# trace back directed cycle
						x = v
						while (x != w):
							self._cycle.append(x)
							x = self._edgeTo[x]
						self._cycle.append(w)
						self._cycle.append(v)
		self._onStack[v] = False


	def cycle(self):
		return self._cycle[::-1]

	def hasCycle(self):
		return self._cycleFound

class EdgeWeightedDC(object):
	"finds first directed cycle in an EdgeWeighted digraph"
	def __init__(self, G):
		self._marked = [False for _ in range(G.V())]
		self._edgeTo = [-1 for _ in range(G.V())]
		self._onStack = [False for _ in range(G.V())]
		self._cycle = []
		self._cycleFound = False
		for v in range(G.V()):
			if self._cycleFound: return
			if not self._marked[v]:
				self._dfs(G, v)

	def _dfs(self, G, v):
		self._marked[v] = True
		self._onStack[v] = True
		if self._cycleFound: return
		else:
			for e in G.adj(v):
				"weighted edges are in adj[v]"
				w = e.sink()
				if not self._marked[w]:
					self._edgeTo[w] = e 
					self._dfs(G, w)
				elif self._onStack[w]:
					# found cycle
					if not self._cycleFound: 
						self._cycleFound = True
						# trace back directed cycle
						while (e.src() != w):
							self._cycle.append(e)
							e = self._edgeTo[e.src()]
						self._cycle.append(e)
		self._onStack[v] = False

	def cycle(self):
		return self._cycle[::-1]


	def hasCycle(self):
		return self._cycleFound





