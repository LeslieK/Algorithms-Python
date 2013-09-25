from GraphLib import EdgeWeightedGraph
from WeightedEdge import Edge
#from UnionFind import UF
from MinSpanTree import KruskalMST

def isEdgeInMST(G, edge):
	"determines whether edge is in MST"
	# create UnionFind data structure
	uf = UF(G.V())

	for f in G.edges():
		if f.weight() < edge.weight():
			v = f.either()
			w = f.other(v)
			if not uf.isConnected(v, w):
				uf.union(v, w)
	v = edge.either()
	w = edge.other(v)
	# check for cycle
	if uf.isConnected(v, w): return False
	return True

def negativeGraph(G):
	"returns graph with negative edge weights"
	Gneg = EdgeWeightedGraph(G.V())
	for e in G.edges():
		# multiply weight by -1
		wt = -e.weight()
		v = e.either()
		w = e.other(v)
		k = Edge(v, w, wt)
		Gneg.addEdge(k)
	return Gneg


def getMinFBset(G):
	Gneg = negativeGraph(G)
	# finds MST of Gneg => max spanning tree of G
	kr = KruskalMST(Gneg)
	allEdges = set(Gneg.edges())
	spanningTreeEdges = set(kr.edges())
	return allEdges - spanningTreeEdges




		





def minFeedbackSet(G):
	"find a minimum-weight feedback edge set"
	# use the process of building a spanning tree to find edges that cause a cycle
	# if the spanning tree has max weight, then the set of feedback edges has min weight
	# the first edge that causes a cycle has min weight and is added to the set

		



