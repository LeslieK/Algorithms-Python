# THIS IS WRONG. WASTED A DAY ON THIS!

# given a digraph: 
# determine whether two vertices are strongly connected
# determine number of strongly connected components
#
# DG = Digraph(13)
# DG.addEdge(0, 5)
# ...
# scc = SCC(DG)
# scc.stronglyConnected(0, 3) => True
# scc.number() => 5
#

from GraphLib import Digraph

class SCC(object):
	def __init__(self, G):
		self._G = G
		self._marked = [False for _ in range(G.V())]
		# initialize each id to its vertex number (only connected to itself)
		self._id = [i for i in range(G.V())]
		for v in range(G.V()):
			self._count = v
			self._cycle = []
			if not self._marked[v]:
				self._dfs(G, v)		
				
	def _dfs(self, G, v):
		self._marked[v] = True
		if self._outdegree(v) == 0:
			# vertex has no out edges
			return
		self._cycle.append(v)
		for w in G.adj(v):
			if not self._marked[w]:
				self._dfs(G, w)
			elif w in self._cycle:
				# cycle detected
				# if cycle begins at index 0, then assign each vertex the min id of any vertex in cycle
				# otherwise, each vertex in cycle is assigned the id of w (the marked vertex)
				print self._cycle, 'w', w
				index = self._cycle.index(w)
				cycle = self._cycle[index:]		
				m = min(cycle)
				if index == 0:
					for i in cycle:
						self._id[i] = self._id[m]
				else:
					for i in cycle:
						# id[w] has already been assigned because w is in the cycle
						self._id[i] = self._id[w] 

	def _outdegree(self, v):
		"return out degree of vertex v"
		return len(self._G.adj(v))

	def _indegree(self, v):
		"return True if vertex has an input edge from some other vertex"
		for e in range(self._G.V()):
			if e != v and v in self._G.adj(e).values():
				return 1
		return 0

	def stronglyConnected(self, v, w):
		return self._id[v] == self._id[w]

	def number(self):
		return len(set(self._id))

DG = Digraph(13)
DG.addEdge(4, 2)
DG.addEdge(2, 3)
DG.addEdge(3, 2)
DG.addEdge(6, 0)
DG.addEdge(0, 1)
DG.addEdge(2, 0)
DG.addEdge(11, 12)
DG.addEdge(12, 9)
DG.addEdge(9, 10)
DG.addEdge(9, 11)
DG.addEdge(10, 12)
DG.addEdge(11, 4)
DG.addEdge(4, 3)
DG.addEdge(3, 5)
DG.addEdge(6, 8)
DG.addEdge(8, 6)
DG.addEdge(5, 4)
DG.addEdge(0, 5)
DG.addEdge(6, 4)
DG.addEdge(6, 9)
DG.addEdge(7, 6)


