# detect a directed cycle in a digraph using DFS
# Find strongly connected components in graph; if V scc, then no cycles
# DG = Digraph(13)
# DG.addEdge(v, w)
# ...
# dc = DirectedCycle(DG)
# dc.cycle()
# returns: 2 0 5 4 2

from KosarajuSharir import SCC

class DirectedCycle(object):
	"find first directed cycle in a digraph"
	def __init__(self, G):
		dc = SCC(G) # runs DFS twice


	def _dfs(self, G, v):
		if not self._cycle:
			self._marked[v] = True
			for w in G.adj(v):
				if not self._marked[w]:
					self._edgeTo[w] = v
					self._dfs(G, w)
				else:
					# found cycle within subgraph
					x = v
					while (x != w):
						self._cycle.append(x)
						x = self._edgeTo[x]
					self._cycle.append(w)
					self._cycle.append(v)
					return

	def cycle(self):
		if not self._cycle:
			print "no cycle"
		else:
			for _ in range(len(self._cycle)):
				print self._cycle.pop()

	def hasCycle(self):
		if not self._cycle:
			return False
		else:
			return True




