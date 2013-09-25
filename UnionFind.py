class UF(object):
	"Builds the Quick Union Find data structure"
	def __init__(self, N):
		"initialize N sites with integers 0 thru N-1"
		self._id = [i for i in range(N)] 		# _id[i] contains the parent node of vertex i
		self._size = [1 for _ in range(N)]		# _size[i] is the number of objects in subtree rooted at i
		self._count = N							# number of connected components

	def union(self, p, q):
		"connect vertices p and q"
		rootp = self.find(p)
		rootq = self.find(q)
		if rootp == rootq:
			return
		if self._size[p] < self._size[q]:
			# connect p's tree to q's tree
			self._id[rootp] = rootq
			self._size[rootq] += self._size[rootp]
		else:
			self._id[rootq] = rootp
			self._size[rootp] += self._size[rootq]
		self._count -= 1

	def find(self, p):
		"identifies component (aka root) for p (0 to N-1)"
		while (p != self._id[p]):
			p = self._id[p]
		return p

	def isConnected(self, p, q):
		"returns true if p and q are in the same component"
		return self.find(p) == self.find(q)

	def count(self):
		"returns the number of connected components"
		return self._count

	def __repr__(self):
		"Everything about UF datastructure"
		return "components=%r id=%r" % (self._count, [p for p in self._id])
