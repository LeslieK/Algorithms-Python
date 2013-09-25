"""
Eulerian cycle. An Eulerian cycle in a graph is a cycle (not necessarily simple) 
that uses every edge in the graph exactly once.

Show that a graph has an Eulerian cycle if and only if it is both connected and every vertex has even degree.
Design a linear-time algorithm to determine whether a graph has an Eulerian cycle, and if so, find one.

A cycle is a path (with at least one edge) whose first and last vertices are the same. 
A simple cycle is a cycle with no repeated edges or vertices (except the requisite repetition of the 
first and last vertices).

e = EC(G)
e.cycle()

"""
from ConnectedComponent import CC

class EC(object):
	def __init__(self, G):
		self._ec = self._isConnected(G) and self._isEvenDegree(G)
		if not self._ec:
			print 'no cycle'
			return
		else:
			# build cycle
			self._edict = {} # dictionary of edges
			self._cycle = [] # list of edges in Eulerian cycle
			# visit each vertex using dfs; mark edges visted
			self._dfs(G, 0)

	def _isConnected(self, G):
		cc = CC(G)
		return cc.count() == 1 

	def _isEvenDegree(self, G):
		"Return True if every vertex has an even degree"
		for v in range(G.V()):
			if sum(G.adj(v).values()) % 2:
				return False
		return True

	def _dfs(self, G, v):
		"run dfs, mark edges visited"
		for w in G.adj(v):
			edge = tuple([v, w])
			if edge not in self._edict:
				self._edict[edge] = True
				if not self._isSelfLoop(edge):
					self._edict[tuple([w, v])] = True
				self._cycle.append(edge)
				self._dfs(G, w)

	def _isSelfLoop(self, edge):
		return edge[0] == edge[1]

	def cycle(self):
		for edge in self._cycle:
			print edge


