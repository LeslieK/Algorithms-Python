from GraphLib import Digraph, EdgeWeightedDigraph
from DirectedEdge import DEdge 

class DFOrder(object):
	def __init__(self, G):
		self._marked = [False for _ in range(G.V())]
		self._post = [] 		# postorder list
		self._pre = [] 			# preorder list
		# run DFS on G; after a vertex is done, push it on a stack
		for v in range(G.V()):
			if not self._marked[v]:
				self._dfs(G, v)

	def _dfs(self, G, v):
		self._pre.append(v) 				
		self._marked[v] = True
		if isinstance(G, Digraph):
			# G.adj(v) is an integer vertex
			for w in G.adj(v):
				if not self._marked[w]:
					self._dfs(G, w)
			# done with v
			self._post.append(v)
		else:
			# G.adj(v) is a directed, weighted edge, DEdge
			for e in G.adj(v):
				w = e.sink()
				if not self._marked[w]:
					self._dfs(G, w)
			# done with v
			self._post.append(v)

	def post(self):
		"return vertices in postorder"
		return self._post

	def reversePost(self):
		"return vertices in reverse postorder"
		return self._post[::-1]

	def pre(self):
		"return vertices in preorder"
		return self._pre




