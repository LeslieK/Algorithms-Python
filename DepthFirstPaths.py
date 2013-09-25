

class DepthFirstSearch(object):
	"depth first search graph processing class"
	def __init__(self, G, source):
		self.marked = [ False for i in range(G.V()) ]
		self.edgeTo = [NaN for i in range(G.V()) ]
		self.dfs(G, source)

	def dfs(self, Graph, v):
		"""
		process graph using depth-first search
		create marked[] and edgeTo[] data structures
		"""
		self.marked[v] = True
		for w in Graph.adj(v):
			if (not self.marked[w]):
				self.dfs(Graph, w)
				self.edgeTo[w] = v

	def hasPathTo(self, v):
		"True if source hasPathTo a vertex v"
		return self.marked[v]

	def pathTo(self, v):
		if not self.hasPath(v): return None
		i = v
		path = []
		while i != source:
			path.append(i)
			i = self.edgeTo[i]
		path.append(source)
		return path.reverse()


