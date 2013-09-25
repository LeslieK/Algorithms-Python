from decimal import Decimal
from DirectedEdge import DEdge
from Topological import TopologicalSort

_INF = -Decimal('infinity')
_SENTINEL = -1

class AcyclicLP(object):
	def __init__(self, G, s):
		"finds the longest path in an edge-weighted DAG (directed acyclic graph) from s to vertex v"
		self._s = s
		self._distTo = [_INF for _ in range(G.V())]
		self._distTo[s] = 0
		self._edgeTo = [_SENTINEL for _ in range(G.V())] # edgeTo[v]: last edge on shortest path from s to v

		# visit vertices in topological order
		top = TopologicalSort(G)
		assert top.isDAG(), 'graph has a cycle'
		# graph is a DAG
		for v in top.order():
			for e in G.adj(v):
				self._relax(e)

	def _relax(self, e):
		"relax edge e"
		v = e.src()
		w = e.sink()
		if self._distTo[w] < self._distTo[v] + e.weight():
			# update data structures
			self._edgeTo[w] = e
			self._distTo[w] = self._distTo[v] + e.weight()

	def distTo(self, v):
		"distance from src to vertex v"
		return self._distTo[v]

	def hasPathTo(self, v):
		"checks whether path exists from src to vertex v"
		return self._edgeTo[v] != _SENTINEL

	def pathTo(self, v):
		"returns path from src to vertex v"
		if not self.hasPathTo(v): return
		path = []
		e = self._edgeTo[v] 				# last edge of path
		while e.src() != self._s:
			path.append(e)
			e = self._edgeTo[e.src()]
		path.append(e)
		return path[::-1]