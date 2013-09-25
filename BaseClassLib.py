from collections import Counter
import random
from WeightedEdge import Edge 	# weighted, undirected
from DirectedEdge import DEdge 	# weighted, directed

class GraphBase(object):
	"defines the base class for a sparse graph"
	def __init__(self, V, E=None):
		"construct a graph"
		self._V = V
		self._E = 0
		self._adj = []
		for _ in range(self._V):
			# bag of weighted edges incident on each vertex
			self._adj.append(Counter())
		# if E:
		# 	# builds a random graph with E edges
		# 	for e in range(E):
		# 		v = int(random.random() * V)
		# 		w = int(random.random() * V)
		# 		self.addEdge(v, w)
		# 		print '{0} to {1}'.format(v, w)

	def V(self):
		"return number of vertices"
		return self._V

	def E(self):
		"return number of edges"
		return self._E

	def adj(self, v):
		"return all edges adjacent to v"
		return self._adj[v]

	@classmethod
	def graphfactory(cls, V, directed=False, weighted=False):
		"returns an instance of the base graph class"
		if not directed and not weighted:
			# undirected, unweighted graph
			def addEdge(self, v, w):
				self._adj[v][w] += 1
				self._adj[w][v] += 1
				self._E += 1

			def edges(self):
				"shows 1 of each edge; if parallel edges, just shows 1 of them"
				edict = {}
				for v in range(self._V):
					for w in self.adj(v):
						if (w, v) not in edict:
							edict[tuple([v, w])] = True
				return [key for key in edict if edict[key]]	
		elif directed and not weighted:
			# directed, unweighted graph (digraph)
			def addEdge(self, v, w):
				self._adj[v][w] += 1
				self._E += 1

			def edges(self):
				"returns list of edges"
				edges = []
				for v in range(self._V):
					for w in self.adj(v):
						edge = '{0} => {1}'.format(v, w)
						edges.append(edge)
				return edges
		elif not directed and weighted:
			# undirected, weighted graph (Edge-weighted graph)
			def addEdge(self, e):
				v = e.either()
				w = e.other(v)
				self._adj[v][e] += 1
				self._adj[w][e] += 1
				self._E += 1

			def edges(self):
				"returns a list of edges"
				edge_list = []
				for v in range(self._V):
					selfLoops = 0
					for e in self._adj[v]:
						if e.other(v) > v:
							edge_list.append(e)
						elif e.other(v) == v:
							if (selfLoops % 2 == 0):
								edge_list.append(e)
								selfLoops += 1
				return edge_list
		else:
			# directed, weighted graph (EdgeWeighted Digraph)
			def addEdge(self, e):
				v = e.src()
				self._adj[v][e] += 1
				self._E += 1

			def edges(self):
				"returns a list of edges"
				edge_list = []
				for v in range(self._V):
					for e in self._adj[v]:
						edge_list.append(e)
				return edge_list
		# add methods to GraphBase class
		cls.addEdge = addEdge
		cls.edges = edges 
		# create graph instance 
		graph = cls(V)
		return graph

# use case:

# from WeightedEdge import Edge 	# weighted, undirected
# from DirectedEdge import DEdge 	# weighted, directed

# class A(GraphBase):
# 	def a_new_method(Self, x):
# 		return x

# a = A.graphfactory(3, directed=True, weighted=False)
# a.addEdge(1, 0)
# a.addEdge(2, 0)
# a.edges()

# b = A.graphfactory(5, directed=True, weighted=True)
# b.addEdge(3, 4)
# b.addEdge(0, 2)
# b.edges()