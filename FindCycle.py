# find cycle in a weighted digraph
from GraphLib import EdgeWeightedDigraph
from DirectedEdge import DEdge 		# directed, weighted edge

# build an edge-weighted digraph
#with open('tinyEWDigraph.txt', 'r') as f:
with open('mediumEWDigraph.txt', 'r') as f:
	V = int(f.readline().strip())
	E = int(f.readline().strip())
	text = f.read()
f.close()
#G = EdgeWeightedDigraph(V)
MG = EdgeWeightedDigraph(V)
lines = text.split('\n')
for line in lines[:-1]:		# last line is empty
	l = line.split()
	v = int(l[0])
	w = int(l[1])
	weight = float(l[2])
	#G.addEdge(DEdge(v, w, weight))
	MG.addEdge(DEdge(v, w, weight))
#print G.E() == E
print MG.E() == E

from DirectedCycle import EdgeWeightedDC
finder = EdgeWeightedDC(MG)
if finder.hasCycle(): finder.cycle()
else: print "no cycle"