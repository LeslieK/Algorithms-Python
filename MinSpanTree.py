from PQ import MinPQ, IndexMinPQ
from UnionFind import UF
from decimal import Decimal
_INF = Decimal('infinity')

class KruskalMST(object):
	"Kruskal's algorithm"
	
	def __init__(self, EG):
		"given a connected, undirected, weighted graph, finds an MST and its weight"
		# list of edges in mst
		self._mst = []
		self._weight = 0
		# build priority queue of edges
		self._pq = MinPQ()
		for e in EG.edges():
			self._pq.insert(e)

		# build union-find data structure
		uf = UF(EG.V())
		while (not self._pq.isEmpty() and len(self._mst) < EG.V() - 1):
			# get next edge from PQ
			e = self._pq.delMin()				# greedily add edges to MST
			v = e.either()
			w = e.other(v)
			if (not uf.isConnected(v, w)):		# edge v-w does not create a cycle
				uf.union(v, w)					# merge components
				self._mst.append(e)				# add edge to MST
				self._weight += e.weight()

	def mst(self):
		"returns edges in MST"
		return self._mst

	def weight(self):
		"returns sum of weights of MST"
		return self._weight

	def __repr__(self):
		"Everything about MST"
		return "edges=%r wt=%r" % ([e for e in self.mst()], self.weight())

class LazyPrimMST(object):
	'''
	given a connected, undirected, weighted graph, finds an MST and its weight
	key = edge; priority = weight of edge
	delete-min to determine next edge to add to to Tree 
	disregard if both endpoints v, w are in T 
	if w is vertex not in T:
	1. add w to T
	2. add edge to T 
	3. add to PQ any edge incident to w (if other endpoint not in T)
	
	PQ has 1 entry per edge
	'''
	def __init__(self, EG):
		self._marked = [False for _ in range(EG.V())]	# MST vertices
		self._mst = []									# list of MST edges
		self._weight = 0
		self._pq = MinPQ()								# MinPQ of edges
		self._visit(EG, 0)

		while (not self._pq.isEmpty() and len(self._mst) < EG.V() - 1):
			e = self._pq.delMin()
			v = e.either(); w = e.other(v)
			if (self._marked[v] and self._marked[w]): continue	# edge is obsolete; both vertices are on Tree
			# add edge to MST list
			self._mst.append(e)
			self._weight += e.weight()
			# visit non-Tree vertex
			if (not self._marked[v]): self._visit(EG, v)
			if (not self._marked[w]): self._visit(EG, w)

	def _visit(self, EG, v):
		"add v to Tree; add each edge e incident on v to PQ if e.other() is not in Tree"
		self._marked[v] = True
		for e in EG.adj(v):
			w = e.other(v)
			if (not self._marked[w]):
				self._pq.insert(e)

	def mst(self):
		"returns edges in MST"
		return self._mst

	def weight(self):
		"returns weight of MST"
		return self._weight

	def __repr__(self):
		"Everything about MST"
		return "edges=%r wt=%r" % (self.mst(), self.weight())

class EagerPrimMST(object):
	'''
	similar to LazyPrimMST except remove obsolete edges from PQ
	given a connected, undirected, weighted graph, finds an MST and its weight
	key = vertex; priority = weight of edge
	PQ has 1 entry per vertex
	'''
	def __init__(self, EG):
		self._edgeTo = [-1 for _ in range(EG.V())]
		self._distTo = [_INF for _ in range(EG.V()) ]
		self._distTo[0] = 0
		self._pq = IndexMinPQ(EG.V())
		self._mst = [] 							# list of edges in MST
		self._weight = 0
		self._marked = set() 					# set of vertices in MST
		self._pq.insert(0, 0)

		while (not self._pq.isEmpty() and len(self._mst) < EG.V() - 1):
			v = self._pq.delMin()
			if v > 0:
				self._mst.append(self._edgeTo[v])
				self._weight += self._edgeTo[v].weight()
			self._visit(EG, v)

	def _visit(self, EG, v):
		'''
		add v to Tree; add all non-tree vertices adjacent to v to PQ; 
		update priority of edges connecting non-tree vertices to Tree
		'''
		self._marked.add(v)
		for e in EG.adj(v):
			# e is edge connecting w (non-Tree vertex) to Tree
			w = e.other(v)
			if w not in self._marked:
				if self._distTo[w] > e.weight():
					self._edgeTo[w] = e
					self._distTo[w] = e.weight()
					if not self._pq.contains(w):
						# w is not in PQ
						self._pq.insert(w, e.weight())
					else:
						self._pq.decreaseKey(w, e.weight())

	def mst(self):
		"returns edges in MST"
		return self._mst

	def weight(self):
		"returns weight of MST"
		return self._weight

	def __repr__(self):
			"Everything about MST"
			return "edges=%r wt=%r" % (self.mst(), self.weight())









		  


	




