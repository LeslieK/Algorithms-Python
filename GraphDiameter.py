"""
Diameter: design a linear-time algorithm 
to find the longest simple path in the graph.
"""

from BreadthFirstSearch import BreadthFirstSearch as BFS
from Cycle import Cycle
from ConnectedComponent import CC

# Return the diameter of a Graph
# diameter = the longest shortest-path


class Diameter(object):
	def __init__(self, G):
		if self._hasCycle(G): 
			print "graph must be acyclic"
			return
		if not G.E(): 
			print 'graph has no edges'
			return 0
		if not self._isConnected(G):
			print 'graph is not connected'
			return
		self._max_dist = -1
		self._marked = [False for _ in range(G.V())]
		self._marked[0] = True
		self._findDiam(G, 0)
	
	def _hasCycle(self, G):
		cycle = Cycle(G)
		return cycle.hasCycle()

	def _isConnected(self, G):
			cc = CC(G)
			return cc.count() == 1

	def _findDiam(self, G, source):
		"find length of longest shortest path"
		abfs = BFS(G, source)
		node = -1
		for v in range(G.V()):
			if abfs.hasPathTo(v):
				dist = abfs.distTo(v)
				if self._max_dist < dist:
					self._max_dist = dist
					node = v # node will be set here at least 1x
		if self._marked[node]:
			# we returned to this vertex from the other end of the longest path
			return self._max_dist
		else:
			# run BFS on node furthest from source
			self._marked[node] = True
			self._findDiam(G, node)

	def diameter(self):
		return self._max_dist			
