# file format: 
# N_jobs
# job_duration	[list of successor jobs]
# ...
from GraphLib import EdgeWeightedDigraph
from DirectedEdge import DEdge 
from LongestPath import AcyclicLP

with open('jobsPC_2.txt', 'r') as f:
#with open('jobsPC.txt', 'r') as f:
	N = int(f.readline().strip()) 						# N is number of jobs to schedule
	# build digraph to model job sequencing: 1 src, 1 target, each job has 2 vertices (start, end)
	G = EdgeWeightedDigraph(N * 2 + 2)
	src = 2*N; sink = 2*N + 1

	lines = f.read().split('\n')						# drop last line which is ''
f.close()
job = 0 												# 'job' is job index
for line in lines:
	fields = line.split() 								# split line on whitepace
	duration = float(fields[0])
	G.addEdge(DEdge(job, job + N, duration))			# add edge betw 'start of job' and 'end of job'
	G.addEdge(DEdge(src, job, 0))
	G.addEdge(DEdge(job + N, sink, 0))
	succ = map(int, fields[1:])
	for w in succ:
		# add precedence edges
		G.addEdge(DEdge(job + N, w, 0))
	job += 1

lp = AcyclicLP(G, src) 									# checks whether G is a DAG
print 'Start times:'
for i in range(N):
	print '%4d: %5.1f\n' % (i, lp.distTo(i))
print 'Finish time: %5.1f\n' % lp.distTo(sink)


		








