# Hamiltonian path in a DAG. Given a directed acyclic graph, 
# design a linear-time algorithm to determine whether it has a 
# Hamiltonian path (a simple path that visits every vertex), and if so, find one.

# From graph, find vertices in topological sorted order (push onto stack)
# This redraws DAG so all paths point upwards
# source = top of stack (bottom of DAG in topologically sorted order)
# target = bottom of stack
# check that each vertex is connected to the one following it, in reverse post order

from DepthFirstOrder import DFOrder

class HAM(object):
	def __init__(self, G):
		dfs = DFOrder(G)
		reverse_post = dfs.reversePost()
		target = reverse_post[-1]
		for v in reverse_post:
			if v != target:
				index = reverse_post.index(v)
				self._marked = [False for _ in range(G.V())]
				self._dfs(G, v)
				next = reverse_post[index+1]
				if not self._marked[next]:
					# v is not connected to the next vertex
					print "no Hamiltonian cycle"
					return
		print "Hamiltonian cycle:", reverse_post

	def _dfs(self, G, v):
		self._marked[v] = True
		for w in G.adj(v):
			if not self._marked[w]:
				self._dfs(G, w)
		# done with v


