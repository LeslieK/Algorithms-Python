# Topological sort is the reverse post order of running DFS on a DAG (Directed Acyclic Graph)

from GraphLib import Digraph, EdgeWeightedDigraph
from DirectedCycle import DC, EdgeWeightedDC 		# unweighted directed cycle finder, edge-weighted directed cycle finder  
from DepthFirstOrder import DFOrder 

class TopologicalSort(object):
	"finds topological order in a digraph or an edge-weighted digraph"
	def __init__(self, G):
		"sorts the vertices of G in reverse DFS postorder"
		self._order = []
		# determine whether G is a digraph or edge-weighted digraph
		if isinstance(G, Digraph):
			finder = DC(G)
		else:
			finder = EdgeWeightedDC(G)
		
		assert not finder.hasCycle(), "graph is not acyclic"
		dfs = DFOrder(G)
		self._order = dfs.reversePost()

	def order(self):
		"returns dfs reverse post order"
		return self._order

	def isDAG(self):
		"True if graph is acylic; otherwise False"
		return self._order != []



