import GraphLib
from BaseClassLib import GraphBase
import DirectedEdge, ShortestPath
import math

with open('rates.txt', 'r') as f:
	V = int(f.readline().strip())
	text = f.read()
f.close()

lines = text.split('\n')

table = []
for line in lines:				
	if len(line) < V+1: continue
	l = line.split()
	name = l[0]
	table.append([name])
	for i in range(1, V+1):
		rate = float(l[i])
		table[-1].append(rate)

# name is vertex-indexed list
name = [table[i][0] for i in range(V)]
#G = GraphLib.EdgeWeightedDigraph(V)
class EWDG(GraphBase):
	pass
G = EWDG.graphfactory(V, directed=True, weighted=True)

for v in range(V):
	for w in range(V):
		if w != v:
			G.addEdge(DirectedEdge.DEdge(v, w, -math.log(table[v][w+1])))

spt = ShortestPath.BellmanFordSP(G, 0)
if (spt.hasNegativeCycle()):
	stake = 1000.00 # the money we want to invest in arbitrage
	for e in spt.negativeCycle():
		# the first negative cycle found
		print "{:10.5f} {:s} ".format(stake, name[e.src()]),
		stake *= math.exp(-e.weight())
		print "= {:10.5f} {:s} ".format(stake, name[e.sink()])
else:
	print "No arbitrage opportunity."


			

			


