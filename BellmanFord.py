import GraphLib
import DirectedEdge, ShortestPath

# negative cycle

with open('tinyEWDnc.txt', 'r') as f:
	V = int(f.readline().strip())
	E = int(f.readline().strip())
	text = f.read()
f.close()

Gnc = GraphLib.EdgeWeightedDigraph(V)
lines = text.split('\n')
for line in lines[:-1]:		# last line is empty
	l = line.split()
	v = int(l[0])
	w = int(l[1])
	weight = float(l[2])
	Gnc.addEdge(DirectedEdge.DEdge(v, w, weight))

# negative weight

with open('tinyEWDn.txt', 'r') as f:
	V = int(f.readline().strip())
	E = int(f.readline().strip())
	text = f.read()
f.close()

Gn = GraphLib.EdgeWeightedDigraph(V)
lines = text.split('\n')
for line in lines[:-1]:		# last line is empty
	l = line.split()
	v = int(l[0])
	w = int(l[1])
	weight = float(l[2])
	Gn.addEdge(DirectedEdge.DEdge(v, w, weight))

bn = ShortestPath.BellmanFord(Gn, 0)
bn.hasNegativeCycle()
bn.hasPathTo(6)
bn.pathTo(6)
bn.distTo(6)