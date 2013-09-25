
from collections import Counter

## build a Graph 
## V = number of vertices
## E = number of edges
class Graph(object):
	"""defines a undirected graph class"""
	def __init__(self, V):
		self._V = V
		self._adj = []
		for v in range(self._V):
			self._adj.append(Counter())

	def addEdge(self, v, w):
		"add edge v - w (parallel edges and self-loops allowed)"
		self._adj[v][w] += 1
		self._adj[w][v] += 1

	def adj(self, v):
		"return all vertices adjacent to v"
		return self._adj[v]

	def V(self):
		"number of vertices"
		return self._V

	def E(self):
		"number of edges (incl self-loops and parallel edges)"
		e = 0
		for v in range(self._V):
			e = sum(self._adj[v].values()) + e
		return e/2

G = Graph(13)
G.addEdge(0, 1)
G.addEdge(0, 2)
G.addEdge(0, 6)
G.addEdge(0, 5)
G.addEdge(6, 4)
G.addEdge(4, 3)
G.addEdge(4, 5)
G.addEdge(3, 5)

G.addEdge(7, 8)
G.addEdge(9, 10)
G.addEdge(9, 11)
G.addEdge(9, 12)
G.addEdge(11, 12)