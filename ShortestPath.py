from decimal import Decimal
from DirectedEdge import DEdge
from PQ import IndexMinPQ
from Topological import TopologicalSort
import collections
import GraphLib, DirectedCycle

_INF = Decimal('infinity')
_SENTINEL = -1

class DijkSP(object):
	def __init__(self, G, s, t = None):
		"find the shortest path tree (in a directed graph with non-negative weights) from s to every other vertex using Dijkstra's alg"
		self._s = s
		self._distTo = [_INF for _ in range(G.V())]
		self._distTo[s] = 0
		self._edgeTo = [_SENTINEL for _ in range(G.V())] # edgeTo[v]: last edge on shortest path from s to v
		self._pq = IndexMinPQ(G.V())
		self._pq.insert(s, 0)

		while (not self._pq.isEmpty()):
			v = self._pq.delMin() 			# add closest vertex to source to Tree
			if t and v == t: return
			for e in G.adj(v):
				self._relax(e) 				# relax(e) updates the distTo and edgeTo data structures					

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

	def _relax(self, edge):
		"relaxes an edge by updating data structures with that edge"
		v = edge.src()
		w = edge.sink()
		if self._distTo[w] > self._distTo[v] + edge.weight():
			self._distTo[w] = self._distTo[v] + edge.weight() 			# distance to source
			self._edgeTo[w] = edge
			if not self._pq.contains(w):
					self._pq.insert(w, self._distTo[w])
			else: 
					self._pq.decreaseKey(w, self._distTo[w])

	def __repr__(self):
		"print spt built by Digjkstra object"
		V = len(self._edgeTo)
		spt = GraphLib.EdgeWeightedDigraph(V)
		for i in range(V):
			if self._edgeTo[i] != _SENTINEL:
				spt.addEdge(self._edgeTo[i])
		print str(spt.edges())

class AcyclicSP(object):
	def __init__(self, G, s):
		"finds the shortest path in an edge-weighted DAG (directed acyclic graph)"
		self._s = s
		self._distTo = [_INF for _ in range(G.V())]
		self._distTo[s] = 0
		self._edgeTo = [_SENTINEL for _ in range(G.V())] # edgeTo[v]: last edge on shortest path from s to v

		# visit vertices in topological order
		top = TopologicalSort(G)
		for v in top.order():
			for e in G.adj(v):
				self._relax(e)

	def _relax(self, e):
		"relax edge e"
		v = e.src()
		w = e.sink()
		if self._distTo[w] > self._distTo[v] + e.weight():
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

class DijkAllPairsSP(object):
	def __init__(self, G):
		"finds shortest path in a directed, edge-weighted graph from source s to target t"
		self._dijkObjs = [DijkSP(G, s) for s in range(G.V())]

	def hasPath(self, s, t):
		"checks whether path exists from s to t"
		return self._dijkObjs[s].hasPath(t)

	def pathTo(self, s, t):
		"returns path from src to vertex v"
		if not self._dijkObjs[s].hasPathTo(t): return
		return self._dijkObjs[s].pathTo(t)

	def distTo(self, s, t):
		"distance from src to vertex v"
		return self._dijkObjs[s].distTo(t) 

class BellmanFordSP(object):
	def __init__(self, G, src):
		"""
		finds shortest path from single source if no negative cycles are reachable from src
		Graph can contain cycles; Graph can contain negative edges
		Does not specify the order in which the vertices are relaxed
		"""
		self._s = src
		self._edgeTo = [_SENTINEL for _ in range(G.V())]
		self._distTo = [_INF for _ in range(G.V())]
		self._distTo[self._s] = 0
		self._q = collections.deque()
		self._onQ = [False for _ in range(G.V())]
		self._q.append(self._s)
		self._onQ[self._s] = True
		self._relaxcount = 0
		self._cycle = []

		while (len(self._q) and self._cycle == []):
			# get next vertex to relax
			v = self._q.popleft()
			self._onQ[v] = False
			self._relax(G, v)

	def _relax(self, G, v):
		"relax vertex"
		for e in G.adj(v):
			# relax edge
			w = e.sink()
			if self._distTo[w] > self._distTo[v] + e.weight():
				self._distTo[w] = self._distTo[v] + e.weight()
				self._edgeTo[w] = e
				if not self._onQ[w]:
					# vertex is not on queue
					self._q.append(w)
					self._onQ[w] = True
			self._relaxcount += 1
			if (self._relaxcount % G.V() == 0):
				# check for cycle after Vth call to relax
				# assert not self.hasNegativeCycle(), "Path from src to v contains negative cycle"
				self._cycle = self._findNegativeCycle()


	def hasPathTo(self, v):
		"returns True if path from src to v exists; otherwise returns False"
		return self._edgeTo != _SENTINEL

	def distTo(self, v):
		"returns length of shortest path from src to v"
		return self._distTo[v]

	def pathTo(self, v):
		"returns shortest path from src to vertex v"
		if not self.hasPathTo(v): return
		path = []
		e = self._edgeTo[v] 				# last edge of path
		while e.src() != self._s:
			path.append(e)
			e = self._edgeTo[e.src()]
		path.append(e)
		return path[::-1]

	def _findNegativeCycle(self):
		"finds a cycle in the SPT, if it exists"
		V = len(self._edgeTo)
		spt = GraphLib.EdgeWeightedDigraph(V)
		for i in range(V):
			# build edge-weighted digraph from edgeTo[]
			if (self._edgeTo[i] != _SENTINEL):
				spt.addEdge(self._edgeTo[i])

		finder = DirectedCycle.EdgeWeightedDC(spt)
		return finder.cycle()

	def hasNegativeCycle(self):
		"returns True if src is connected to a negative cycle"
		return self._findNegativeCycle() != []

	def negativeCycle(self):
		"returns a negative cycle, if one exists"
		return self._findNegativeCycle()

	def __repr__(self):
		"print spt built by BellmanFordSP object"
		V = len(self._edgeTo)
		spt = GraphLib.EdgeWeightedDigraph(V)
		for i in range(V):
			if self._edgeTo[i] != _SENTINEL:
				spt.addEdge(self._edgeTo[i])
		return str(spt.edges())


