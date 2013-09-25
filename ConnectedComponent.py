# Finding connected components in a graph with DFS

class CC(object):
	def __init__(self, G):
		self._marked = [False for i in range(G.V())]
		self._id = [-1 for i in range(G.V())]
		self._count = 0

		for v in range(G.V()):
			if not self._marked[v]:
				self.dfs(G, v)
				self._count += 1

	def count(self):
		"returns the number of connected components"
		return self._count

	def id(self, v):
		"returns the connected component for vertex v"
		return self._id[v]

	def dfs(self, G, v):
		"""all vertices discovered in same dfs() call are in same component
		dfs() just sets id
		"""
		self._marked[v] = True
		self._id[v] = self._count
		for w in G.adj(v):
			#w is adjacent to v
			if not self._marked[w]:
				self.dfs(G, w)


