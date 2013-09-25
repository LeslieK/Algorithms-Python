# checks whether a graph contains a cycle
from GraphLib import Graph

class Cycle(object):
	def __init__(self, G):
		"find whether graph has a cycle"
		if self._hasSelfLoop(G): 
			self._cycleFound = True
			return
		if self._hasParallelLoop(G): 
			self._cycleFound = True 
			return
		self._marked = [False for i in range(G.V())]
		self._cycleFound = False
		# run dfs on each node
		for v in range(G.V()):
			if not self._marked[v]:
				self._dfs(G, -1, v)

	def hasCycle(self):
		return self._cycleFound

	def _hasSelfLoop(self, G):
		"edge from vertex to itself"
		for v in range(G.V()):
			for w in G.adj(v):
				if w == v: return True
		return False

	def _hasParallelLoop(self, G):
		"parallel loop: 2 edges between v and w"
		self._marked = [False for i in range(G.V())]
		for v in range(G.V()):
			for w in G.adj(v):
				if not self._marked[w]:
					self._marked[w] = True
				else:
					return True
			for w in G.adj(v):
				self._marked[w] = False
		return False

	def _dfs(self, G, fromNode, v):
		"determine whether Graph has a cycle"
		self._marked[v] = True
		for w in G.adj(v):
			if not self._marked[w]:
				self._dfs(G, v, w)
			elif fromNode != w:
				# w was visited from some other vertex other than fromNode
				self._cycleFound = True

# Test a graph with a cycle
# G = Graph(13)
# G.addEdge(0, 1)
# G.addEdge(0, 2)
# G.addEdge(0, 6)
# G.addEdge(0, 5)
# G.addEdge(6, 4)has
# G.addEdge(4, 3)
# G.addEdge(4, 5)
# G.addEdge(3, 5)

# G.addEdge(7, 8)
# G.addEdge(9, 10)
# G.addEdge(9, 11)
# G.addEdge(9, 12)
# G.addEdge(11, 12)

# Test a graph with no cycle
Gacyc = Graph(8)
Gacyc.addEdge(0, 1)
Gacyc.addEdge(0, 2)
Gacyc.addEdge(2, 3)
Gacyc.addEdge(2, 4)
Gacyc.addEdge(4, 5)
Gacyc.addEdge(5, 6)
Gacyc.addEdge(5, 7)

G = Gacyc

c = Cycle(G)
c.hasCycle()
