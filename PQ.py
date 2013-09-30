class MinPQ(object):
	"min priority queue; min value removed first"
	def __init__(self):
		"Builds a MinPQ data structure"
		self._pq = [0]					# store items at indices 1 to N
		self._N = 0						# number of items on PQ

	def isEmpty(self):
		return self._N == 0

	def size(self):
		return self._N

	def insert(self, x):
		"add x to PQ; swim it up to maintain heap invariant"
		self._N += 1
		self._pq.append(x)
		self._swim(self._N)

	def delMin(self):
		"delete and return the smallest key in PQ"
		if self.isEmpty():
			return "No such element exception"
		else:
			self._exch(1, self._N)
			minkey = self._pq.pop()
			self._N -= 1
			self._sink(1)
			return minkey

	# helper functions to restore heap invariant
	def _swim(self, k):
		"move key in position k up to maintain heap invariant"
		while (k > 1 and self._greater(k/2, k)):
			self._exch(k, k/2)
			k = k/2

	def _sink(self, k):
		"move key in position k down to maintain heap invariant"
		while(2 * k <= self._N):
			# consider the children of k
			j = 2*k
			# get the smallest child
			if (j < self._N and self._greater(j, j+1)):
				j += 1
			# check that parent k < child j
			if (not self._greater(k, j)): break
			self._exch(j, k)
			k = j

	def _exch(self, k1, k2):
			swap = self._pq[k1]
			self._pq[k1] = self._pq[k2]
			self._pq[k2] = swap

	def _greater(self, k1, k2):
		#return self._pq[k1].weight() > self._pq[k2].weight()
		return self._pq[k1].compareTo(self._pq[k2]) == 1

	def __repr__(self):
		"Uniquely identifies MinPQ"
		return "size=%r weights=%r" % (self.size(), [key.weight() for key in self._pq[1:]])


class MaxPQ(object):
	"max priority queue; max value removed first"
	def __init__(self):
		"Builds a MinPQ data structure"
		self._pq = [0]					# store items at indices 1 to N
		self._N = 0						# number of items on PQ

	def isEmpty(self):
		return self._N == 0

	def size(self):
		return self._N

	def insert(self, x):
		"add x to PQ; swim it up to maintain heap invariant"
		self._N += 1
		self._pq.append(x)
		self._swim(self._N)

	def delMax(self):
		"delete and return the smallest key in PQ"
		if self.isEmpty():
			return "No such element exception"
		else:
			self._exch(1, self._N)
			minkey = self._pq.pop()
			self._N -= 1
			self._sink(1)
			return minkey

	# helper functions to restore heap invariant
	def _swim(self, k):
		"move key in position k up to maintain heap invariant"
		while (k > 1 and self._lessthan(k/2, k)):
			self._exch(k/2, k)
			k = k/2

	def _sink(self, k):
		"move key in position k down to maintain heap invariant"
		while(2 * k <= self._N):
			# consider the children of k
			j = 2*k
			# get the smallest child
			if (j < self._N and self._lessthan(j, j+1)):
				j += 1
			# check that parent k < child j
			if (not self._lessthan(k, j)): break
			self._exch(j, k)
			k = j

	def _exch(self, k1, k2):
			swap = self._pq[k1]
			self._pq[k1] = self._pq[k2]
			self._pq[k2] = swap

	def _lessthan(self, k1, k2):
		#return self._pq[k1].weight() < self._pq[k2].weight()
		return self._pq[k1].compareTo(self._pq[k2]) < 1

	def __repr__(self):
		"Uniquely identifies MaxPQ"
		return "size=%r weights=%r" % (self.size(), [e.weight() for e in self._pq[1:]])

class IndexMinPQ(object):
	"min priority queue where each key is referenced by an index i"
	def __init__(self, N):
		"create indexed PQ with indices 0 thru N-1"
		self._NMAX = N                          # max number of keys
		self._keys = [-1 for _ in range(N+1)] 	# key = priority (ex: weight of an edge)
		self._pq = [-1 for _ in range(N+1)]		# input: heap position 		output: index
		self._qp = [-1 for _ in range(N+1)]		# input: index 				output: heap position 
		self._N = 0								# size of _pq

	def insert(self, i, key): 					# internal to class, index range is 1 thru NMAX	
		assert ((i >= 0 and i < self._NMAX) == True), "i is out of bounds"									
		if (not self.contains(i)): 				# contains parameter is indexed from 0
			self._N = self._N + 1				# add 1 to number of elements in PQ
			self._pq[self._N] = i + 1 			# index is stored on pq at heap position N
			self._qp[i + 1] = self._N 			# index is stored at heap position N
			self._keys[i + 1] = key
			self._swim(self._N)
		else:
			print "index is already in PQ"

	def size(self):
		return self._N

	def isEmpty(self):
		return self._N == 0

	def minIndex(self):
		"return index associated with minimal key"
		return self._pq[1] - 1	# min index is stored in heap position 1; subtract 1 so indexing is from 0

	def minKey(self):
		"return minimal key"
		return self._keys[self._pq[1]]

	def decreaseKey(self, i, key):
		"decrease the key associated with index i to the specified value"
		assert (i >= 0 and i < self._NMAX) == True, "i out of range"
		if (self.contains(i)): 				# 'contains' parameter is indexed from 0
			self._keys[i+1] = key
			self._swim(self._qp[i+1])		# qp[i] is the heap position; since key is less than original key, swim it up
		else:
			print "index is not in PQ"

	def delMin(self):
		"delete a minimal key and return its associated index"
		assert self._N > 0
		if (self._N > 0):
			min_index = self._pq[1]
			self._exch(1, self._N)
			self._keys[min_index] = -1 		# remove key from keys
			self._pq[self._N] = -1 			# remove index from PQ
			self._qp[min_index] = -1 		# free heap position in heap
			self._N = self._N - 1			# reduce size of PQ by 1
			self._sink(1) 					# heapify heap
			return min_index - 1 			# subtract 1 so indexing is from 0

	def contains(self, i):
		"test whether pq contains index i"
		assert (i >= 0 and i < self._NMAX) == True, "i out of range"
		return self._qp[i + 1] != -1 		# -1 means heap position has not been assigned

	def keyOf(self, i):
		"returns key associated with index i"
		assert (i >= 0 and i < self._NMAX) == True, "i out of range"
		if self.contains(i):
			return self._keys[i+1]
		else:
			print "index is not in PQ"

	def __repr__(self):
		"Uniquely identifies IndexMinPQ"
		return "size=%r indices=%r keys=%r" % (self.size(), self._pq[1:], self._keys[1:])


	def _greater(self, i, j):
		"i, j are heap positions"
		return self._keys[self._pq[i]] > self._keys[self._pq[j]]

	def _exch(self, i, j):
		"i, j are heap positions"
		# exch indexes in pq
		swap = self._pq[i] 			# index in heap position i is copied to swap
		self._pq[i] = self._pq[j]	# index in heap position j is copied into heap position i
		self._pq[j] = swap 			# swap is copied to heap position j
		# update heap positions for these indexes in qp
		self._qp[self._pq[i]] = i 	# update qp with heap position for index pq[i]
		self._qp[self._pq[j]] = j	# update qp with heap position for index pq[j]


	def _swim(self, k):
		'''
		k is position in heap
		swim key up in heap to maintain heap invariant
		'''
		while (k > 1 and self._greater(k/2, k)):
			self._exch(k, k/2)
			k = k/2

	def _sink(self, k):
		'''
		k is position in heap
		sink key down in heap to maintain heap invariant
		'''
		while (2*k <= self._N):								# check that node in heap position k has a child
			j = 2 * k 										# j is heap position of child
			if (j < self._N and self._greater(j, j+1)): 	# set j to smallest child
				j = j + 1
			if (not self._greater(k, j)): break				# compare parent to smallest child
			else:
				self._exch(k, j)
				k = j 										# set parent to heap position of child and repeat sink
