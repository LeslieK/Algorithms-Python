class Edge(object):
	"defines an undirected, weighted edge"
	def __init__(self, v, w, wt):
		self.v = v
		self.w = w
		self.wt = wt

	def either(self):
		return self.v

	def other(self, v):
		if v == self.v:
			return self.w
		else:
			return self.v

	def compareTo(self, that):
		if (self.wt < that.weight()):
			return -1
		elif (self.wt > that.weight()):
			return 1
		else:
			return 0

	def weight(self):
		return self.wt

	def __repr__(self):
		"This is everything you need to know about an edge"
		return "Edge(v=%r, w=%r, wt=%r)" % (self.v, self.w, self.wt)



