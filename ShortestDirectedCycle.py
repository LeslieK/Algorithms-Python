# DIRECTED GRAPHS
# Question 1
# Shortest directed cycle. Given a digraph G, design an efficient algorithm to find a directed cycle 
# with the minimum number of edges (or report that the graph is acyclic). The running time of your 
# algorithm should be at most proportional to V(E+V) and use space proportional to E+V, where V is 
# the number of vertices and E is the number of edges.

# shorted directed cycle
# sdc = SDC(DG)
# sdc.cycle()

from collections import deque
from decimal import Decimal
_inf = Decimal('infinity')

class SDC(object):
	"finds the shortest directed cycle"
	def __init__(self, G):
		
		self._cycles = []
		self._q = deque()
		for v in range(G.V()):
			# run bfs from each vertex
			self._q.clear()
			self._edgeTo = [-1 for _ in range(G.V())]
			self._distTo = [_inf for _ in range(G.V())]
			self._marked = [False for _ in range(G.V())]
			self._marked[v] = True
			self._distTo[v] = 0
			self._q.append(v)
			self._bfs(G, v)

	def _bfs(self, G, s):
		"finds shortest cycle from v"
		while len(self._q) > 0:
			v = self._q.pop()
			for w in G.adj(v):
				if not self._marked[w]:
					self._marked[w] = True
					self._distTo[w] = self._distTo[v] + 1
					self._edgeTo[w] = v
					self._q.append(w)
				else:
					# visited w before; check if it equals the source
					if w == s:
						# found shortest cycle from source
						cycle = self._build_cycle(v, w)
						self._cycles.append(cycle)
						return
		# no cycles from s


	def _build_cycle(self, v, w):
		cycle = []
		x = v
		while x != w:
			cycle.append(x)
			x = self._edgeTo[x]
		cycle.append(w)
		cycle.append(v)
		return cycle

	def cycle(self):
		if not self._cycles:
			print "No cycle"
		else:
			cycle_reversed = min(self._cycles, key = len)
			print cycle_reversed[::-1]








		

