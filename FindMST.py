from GraphLib import EdgeWeightedGraph
from WeightedEdge import Edge
from MinSpanTree import KruskalMST, LazyPrimMST, EagerPrimMST

with open('mediumEdgeWeightedGraph.txt', 'r') as f:
	V = int(f.readline().strip())
	E = int(f.readline().strip())
	text = f.read()
f.close()
G = EdgeWeightedGraph(V)
lines = text.split('\n')
for line in lines[:-1]:		# last line is empty
	l = line.split()
	v = int(l[0])
	w = int(l[1])
	weight = float(l[2])
	G.addEdge(Edge(v, w, weight))
print G.E() == E

k = KruskalMST(G)
l = LazyPrimMST(G)
e = EagerPrimMST(G)
k.weight()
l.weight()
e.weight()

import cProfile, pstats
cProfile.run('KruskalMST(G)', 'kstats')
cProfile.run('LazyPrimMST(G)', 'lstats')
cProfile.run('EagerPrimMST(G)', 'estats')
kp = pstats.Stats('kstats')
kp.strip_dirs().sort_stats('cumulative').print_stats(10)
lp = pstats.Stats('lstats')
lp.strip_dirs().sort_stats('cumulative').print_stats(10)
ep = pstats.Stats('estats')
ep.strip_dirs().sort_stats('cumulative').print_stats(10)

