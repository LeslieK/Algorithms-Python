# Reachable vertex.
# DAG: Design a linear-time algorithm to determine whether a DAG has a vertex that 
# is reachable from every other vertex, and if so, find one.
# Get topological sorted order; run DFS from each vertex; 
# if target is in each marked list => target vertex, otherwise None

# Digraph: Design a linear-time algorithm to determine whether a 
# digraph has a vertex that is reachable from every other vertex, and if so, find one.
# run dfs from every vertex => V marked lists, one for each vertex
# take intersection of these lists => if []: None, otherwise:vertices that every vertex can reach
#
# rcc = Reach(DG) => returns vertices, or "no vertex..."

from DirectedCycle import DC
from DepthFirstOrder import DFOrder

class Reach(object):
	def __init__(self, G):
		self._all_marked_lists = []
		dc = DC(G)
		if dc.hasCycle():
			# digraph with cycle
			for v in range(G.V()):
				self._marked = [False for _ in range(G.V())]
				self._dfs(G, v)
				self._all_marked_lists.append(self._marked)
			# done running DFS on vertices; find intersection of all marked lists
			all_lists = [[i for i in range(G.V()) if alist[i] is True] for alist in self._all_marked_lists]
			final = set(all_lists[0])
			for s in all_lists[1:]:
				ss = set(s)
				final = final.intersection(ss)
			if not final:
				print "no vertex is reachable from all other vertices"
			else:
				for i in final:
					print i
		else:
			# DAG
			# only the target vertex is a candidate for being reachable
			dfs = DFOrder(G)
			reverse_post = dfs.reversePost()
			target = reverse_post[-1]
			for v in reverse_post:
				if v != target:
					self._marked = [False for _ in range(G.V())]
					self._dfs(G, v)
					self._all_marked_lists.append(set(self._marked))
			# done running DFS on vertices; target must be in all marked lists
			for markedList in self._all_marked_lists:
				if target not in markedList:
					print "no vertex is reachable from all other vertices"
					return
			print target

	def _dfs(self, G, v):
		self._marked[v] = True
		for w in G.adj(v):
			if not self._marked[w]:
				self._dfs(G, w)







