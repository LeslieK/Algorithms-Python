from collections import deque
from decimal import Decimal
_inf = Decimal('infinity')

class BreadthFirstSearch(object):
	def __init__(self, G, source):
		self._q = deque()
		self._marked = [ False for i in range(G.V()) ]
		self._edgeTo = [-1 for i in range(G.V()) ]
		self._distTo = [_inf for i in range(G.V())]
		self._bfs(G, source)


	def _bfs(self, G, source):
		"find all paths from one or more sources"
		if self.isIterable(source):
			"multiple sources"
			for s in source:
				self._q.append(s)
				self._marked[s] = True
				self._distTo[s] = 0
		else:
			"single source"
			self._q.append(source)
			self._marked[source] = True
			self._distTo[source] = 0
		while len(self._q) > 0:
			v = self._q.popleft()
			for w in G.adj(v):
				if not self._marked[w]:
					self._q.append(w)
					self._marked[w] = True
					self._edgeTo[w] = v
					self._distTo[w] = self._distTo[v] + 1

	def hasPathTo(self, v):
		return self._marked[v]

	def distTo(self, v):
		return self._distTo[v]

	def pathTo(self, v):
		"returns path from source to v"
		if not self.hasPathTo(v): return None
		i = v
		path = []
		while self._distTo[i] != 0:
			path.append(i)
			i = self._edgeTo[i]
		path.append(i)
		return path[::-1]

	def isIterable(self, obj):
		return hasattr(obj, '__contains__')


			



