

class DepthFirstSearch(object):
	"depth first search graph processing class"
	def __init__(self, G, source):
		self._source = source
		self._marked = [ False for i in range(G.V()) ]
		self._edgeTo = [-1 for i in range(G.V()) ]
		self._dfs(G, source)

	def _dfs(self, Graph, v):
		"""
		process graph using depth-first search
		create marked[] and edgeTo[] data structures
		"""
		self._marked[v] = True
		for w in Graph.adj(v):
			if (not self._marked[w]):
				self._dfs(Graph, w)
				self._edgeTo[w] = v

	def hasPathTo(self, v):
		"True if source hasPathTo a vertex v"
		return self._marked[v]

	def pathTo(self, v):
		"returns path from source to v"
		if not self.hasPathTo(v): return None
		i = v
		path = []
		while i != self._source:
			path.append(i)
			i = self._edgeTo[i]
		path.append(self._source)
		return path[::-1]


