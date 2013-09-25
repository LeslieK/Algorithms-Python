class DEdge(object):
	"defines a directed, weighted edge"
	def __init__(self, v, w, weight):
		self._v = v
		self._w = w
		self._wt = weight

	def src(self):
		return self._v

	def sink(self):
		return self._w

	def weight(self):
		return self._wt

	def compareTo(self, that):
		if (self._wt < that.weight()):
			return -1
		elif (self._wt > that.weight()):
			return 1
		else:
			return 0

	def __repr__(self):
		"This is everything you need to know about a weighted directed edge"
		#Edge(from=%r, to=%r, wt=%r)" % (self._v, self._w, self._wt)
		return "%r -> %r %r " % (self._v, self._w, self._wt)


