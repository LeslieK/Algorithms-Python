"""
Center: design a linear-time algorithm to find a 
vertex such that its maximum distance from any 
other vertex is minimized.
"""
from BreadthFirstSearch import BreadthFirstSearch as BFS
from Cycle import Cycle
from ConnectedComponent import CC

class Center(object):
	def __init__(self, G):
		if self._hasCycle(G): 
			print "graph must be acyclic"
			return
		if not G.E():
			print "graph has no edges"
			return
		if not self._isConnected(G):
			print 'graph is not connected'
			return
		self._maxdistances = [0 for _ in range(G.V())]
		self._findCenter(G)

	def _isConnected(self, G):
			cc = CC(G)
			return cc.count() == 1

	def _hasCycle(self, G):
		cycle = Cycle(G)
		return cycle.hasCycle()

	def _findCenter(self, G):
		for source in range(G.V()):
			maxdist = 0
			abfs = BFS(G, source)
			for v in range(G.V()):
				if abfs.hasPathTo(v):
					dist = abfs.distTo(v)
					if maxdist < dist:
						maxdist = dist
			self._maxdistances[source] = maxdist

	def center(self):
		"return vertex with shortest max distance to other vertices"
		minmaxdist = min(self._maxdistances)
		return self._maxdistances.index(minmaxdist)

