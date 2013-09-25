
from collections import Counter
import random
from WeightedEdge import Edge 	# weighted, undirected
from DirectedEdge import DEdge 	# weighted, directed

## build a Graph 
## V = number of vertices
## E = number of edges

class Graph(object):
	"""defines an undirected graph"""
	def __init__(self, V, E=None):
		self._V = V
		self._adj = []
		for v in range(self._V):
			self._adj.append(Counter())
		if E:
			# builds a random graph with E edges
			for e in range(E):
				v = int(random.random() * V)
				w = int(random.random() * V)
				self.addEdge(v, w)
				print '{0} to {1}'.format(v, w)	

	def addEdge(self, v, w):
		"add edge v - w (parallel edges and self-loops allowed)"
		self._adj[v][w] += 1
		self._adj[w][v] += 1

	def adj(self, v):
		"return all vertices adjacent to v"
		return self._adj[v]

	def V(self):
		"number of vertices"
		return self._V

	def E(self):
		"number of edges (incl self-loops and parallel edges)"
		e = 0
		for v in range(self._V):
			e = sum(self._adj[v].values()) + e
		return e/2

	def _isSelfLoop(self, v, w):
		return v == w

	def showEdges(self):
		"shows 1 of each edge; if parallel edges, just shows 1 of them"
		edict = {}
		for v in range(self._V):
			for w in self.adj(v):
				if (w, v) not in edict:
					edict[tuple([v, w])] = True
					print '{0} to {1}'.format(v, w)

	def removeEdge(self, v, w):
		if w not in self.adj(v):
			print "no such edge"
		else:
			self._adj[v][w] -= 1
			self._adj[w][v] -= 1
			if not self._adj[v][w]:
				del(self._adj[v][w])
				del(self._adj[w][v])

	def __repr__(self):
		"Everything about an undirected graph"
		return "Graph(V=%r, E=%r)" % (self.V(), self.E())

class Digraph(object):
	"""defines a directed, unweighted graph"""
	def __init__(self, V):
		self._V = V
		self._adj = []
		for v in range(self._V):
			self._adj.append(Counter())

	def addEdge(self, v, w):
		"add edge v - w (parallel edges and self-loops allowed)"
		self._adj[v][w] += 1

	def adj(self, v):
		"return all vertices adjacent to v"
		return self._adj[v]

	def V(self):
		"number of vertices"
		return self._V

	def E(self):
		"number of edges (incl self-loops and parallel edges)"
		e = 0
		for v in range(self._V):
			e = sum(self._adj[v].values()) + e
		return e

	def _isSelfLoop(self, v, w):
		return v == w

	def showEdges(self):
		"shows each directed edge"
		for v in range(self._V):
			for w in self.adj(v):
				print '{0} -> {1}'.format(v, w)

	def edges(self):
		"returns list of edges"
		edges = []
		for v in range(self._V):
			for w in self.adj(v):
				edge = '{0} => {1}'.format(v, w)
				edges.append(edge)
		return edges


	def removeEdge(self, v, w):
		if w not in self.adj(v):
			print "no such edge"
		else:
			self._adj[v][w] -= 1
			if not self._adj[v][w]:
				del(self._adj[v][w])

	def reverse(self):
		R = Digraph(self._V)
		for v in range(self._V):
			for w in self._adj[v]:
				R.addEdge(w, v)
		return R

	def __repr__(self):
		"Everything you need to know about a digraph"
		return "Digraph(V=%r, E=%r, edges=%r)" % (self.V(), self.E(), self.edges())


class EdgeWeightedGraph(object):
	"An undirected graph with weighted edges"
	def __init__(self, V=None, EG=None):
		if V:
			# constructs a graph
			self._V = V
			self._E = 0
			self._adj = []
			for _ in range(self._V):
				# bag of weighted edges incident on each v
				self._adj.append(Counter())
		elif EG:
			# constructs a copy of graph EG
			self._V = EG.V()
			self._E = EG.E()
			self._adj = []
			for v in range(self._V):
				self._adj.append(EG.adj(v))
		else:
			return "Error: missing argument"

	def V(self):
		return self._V

	def E(self):
		return self._E

	def addEdge(self, e):
		"add weighted edge v-w to graph"
		v = e.either()
		w = e.other(v)
		self._adj[v][e] += 1
		self._adj[w][e] += 1
		self._E += 1

	def adj(self, v):
		"return all edges incident on v"
		return self._adj[v]

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

	def __repr__(self):
		"Everything you need to know about a weighted graph"
		return "V=%r, E=%r, edges=%r" % (self._V, self._E, [e for e in self.edges()])

		
class EdgeWeightedDigraph(object):
	"a directed graph with weighted edges"
	def __init__(self, V=None, EG=None):
		if V:
			# constructs a graph
			self._V = V
			self._E = 0
			self._adj = []
			for _ in range(self._V):
				# bag of weighted edges incident on each v
				self._adj.append(Counter())
		elif EG:
			# constructs a copy of graph EG
			self._V = EG.V()
			self._E = EG.E()
			self._adj = []
			for v in range(self._V):
				self._adj.append(EG.adj(v))
		else:
			return "Error: missing argument"

	def V(self):
		"returns number of vertices"
		return self._V

	def E(self):
		"returns number of edges"
		return self._E

	def addEdge(self, e):
		"add weighted edge v->w to graph"
		v = e.src()
		self._adj[v][e] += 1
		self._E += 1

	def adj(self, v):
		"return all edges incident on v"
		return self._adj[v]

	def edges(self):
		"returns a list of edges"
		edge_list = []
		for v in range(self._V):
			for e in self._adj[v]:
				edge_list.append(e)
		return edge_list

	def __repr__(self):
		"Everything you need to know about a weighted digraph"
		return "V=%r, E=%r, edges=%r" % (self._V, self._E, [e for e in self.edges()])




