from GraphLib import EdgeWeightedDigraph
from BaseClassLib import GraphBase
from DirectedEdge import DEdge 		# directed, weighted edge
from LongestPath import AcyclicLP 
from ShortestPath import AcyclicSP	

with open('tinyEWDAG.txt', 'r') as f:
	V = int(f.readline().strip())
	E = int(f.readline().strip())
	text = f.read()
f.close()

#dag = EdgeWeightedDigraph(V)
class DAG(GraphBase):
	pass
dag = DAG.graphfactory(V, directed=True, weighted=True)
lines = text.split('\n')
for line in lines[:-1]:		# last line is empty
	l = line.split()
	v = int(l[0])
	w = int(l[1])
	weight = float(l[2])
	dag.addEdge(DEdge(v, w, weight))

#find the longest path from 0 => 5
d = AcyclicLP(dag, 5)
d.distTo(0)

#find the shortest path from 0 => 5
sh = AcyclicSP(dag, 5)
sh.distTo(0)