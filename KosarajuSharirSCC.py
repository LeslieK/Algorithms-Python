# Finding connected components in a graph with DFS
from DepthFirstOrder import DFOrder

class SCC(object):
	def __init__(self, G):
		self._marked = [False for i in range(G.V())]
		self._id = [-1 for i in range(G.V())]
		self._count = 0

		# run DFS once on the reverse Graph!
		dfs = DFOrder(G.reverse())
		# run DFS again on original Graph using reverse post order
		for v in dfs.reversePost():
			if not self._marked[v]:
				self._dfs(G, v)
				self._count += 1

	def count(self):
		"returns the number of connected components"
		return self._count

	def id(self, v):
		"returns the connected component for vertex v"
		return self._id[v]

	def isSCC(self, v, w):
		return self._id[v] == self._id[w]

	def _dfs(self, G, v):
		"""all vertices discovered in same dfs() call are in same component
		dfs() just sets id
		"""
		self._marked[v] = True
		self._id[v] = self._count
		for w in G.adj(v):
			#w is adjacent to v
			if not self._marked[w]:
				self._dfs(G, w)


