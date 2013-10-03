from decimal import Decimal
_INF = Decimal('infinity')
_SENTINEL = -1
_BORDER_ENERGY = 195075

class SeamCarver(object):
	"removes seams from an image"
	def __init__(self, picture):
		self._img = picture.imageArray
		self._height = picture.num_rows
		self._width = picture.num_cols
		self._num_channels = picture.num_channels
		self._energy = picture.energyArray
		
		# virtual source and sink vertices
		self._num_pixels = self._height * self._width
		self._source = self._num_pixels
		self._sink = self._source + 1

		# graph data structures
		self._edgeTo = [_SENTINEL for _ in range(self._num_pixels + 2)]	# add 2 for source, sink pixels
		self._distTo = [_INF for _ in range(self._num_pixels + 2)]

	def width(self):
		return self._width

	def height(self):
		return self._height

	def energy(self, col, row):
		"return energy of pixel in (col, row)"
		if self._isValid(col, row):
			return self._energy[self._toLinear(col, row)]

	def findVerticalSeam(self):
		"return vertical seam in image"
		# vertical seam = sequence of cols; seam[0] is col of row 0
		# row-indexed seam
		seam = [-1 for _ in range(self._height)]
		self._buildGraph()
		row = self._height - 1
		v = self._edgeTo[self._sink]
		while (v != self._source):
			seam[row] = v % self._width  # seam[row] = col
			v = self._edgeTo[v]
			row -= 1
		return seam

	def findHorizontalSeam(self):
		"return horizontal seam in image"
		# tranpose dimensions
		self._exchDims()

		# horizontal seam = sequence of rows; seam[0] is row of col 0
		# col-indexed seam
		seam = [-1 for _ in range(self._height)]
		self._buildGraph(transposed=True)
		row = self._height - 1
		v = self._edgeTo[self._sink]
		while (v != self._source):
			seam[row] = v % self._width  # seam[row] = col
			v = self._edgeTo[v]
			row -= 1
		self._exchDims()
		return seam

	def _exchDims(self):
		"exchange self._width and self._height"
		swap = self._width
		self._width = self._height
		self._height = swap

	def _toLinear(self, col, row):
		"converts pixel from (col, row) to single index"
		if self._isValid(col, row):
			return row * self._width + col

	def _toGrid(self, num):
		"converts pixel from single index to (col, row)"
		if self._isValid(num):
			row = num / self._width
			col = num % self._width
			return (col, row)

	def _isValid(self, col, row=None):
		if row is None:
			if (col < 0) or (col > self._width * self._height - 1):
				return False
			else:
				return True
		else:
			if (col < 0) or (col > self._width-1) or (row < 0) or (row > self._height-1):
				return False
			else:
				return True

	def _buildGraph(self, transposed=False):
		"pixels are nodes; edges define precedence constraints in a seam"
		
		# for row 0 pixels: distTo[] is 0; edgeTo[] is _source vertex 
		for i in range(0, self._width):
			self._distTo[i] = 0
			self._edgeTo[i] = self._source
		# distTo[] is 0 for source pixel
		self._distTo[self._num_pixels] = 0

		# for each vertex (pixel), calculate edgeTo[], distTo[]
		# start at row 1
		for v in range(self._width, self._num_pixels):
			if (v % self._width == 0):
				# pixel is on left edge
				self._edgeTodistTo(v, transposed=transposed, edgeL=True)
			elif (v % self._width == self._width - 1):
				# pixel is on right edge
				self._edgeTodistTo(v, transposed=transposed, edgeR=True)
			else:
				self._edgeTodistTo(v, transposed=transposed)
		# for sink vertex
		index, min_energy = min(enumerate(self._distTo[self._num_pixels - self._width:self._num_pixels]), key=lambda (x, y): y)
		self._distTo[self._sink] = min_energy
		self._edgeTo[self._sink] = (self._height - 1) * self._width + index


	def _edgeTodistTo(self, v, edgeL=False, edgeR=False, transposed=False):
		# returns pixel connected to v with min energy

		if edgeL:
			# left edge
			vC = v - self._width
			vRD = v - self._width + 1
			vLU = vC
		elif edgeR:
			# right edge
			vLU = v - self._width - 1
			vC = v - self._width
			vRD = vC
		else:
			# pixels connect to v
			vLU = v - self._width - 1
			vC = v - self._width
			vRD = v - self._width + 1
		# energy of pixels connected to v
		if transposed:
			(colU, rowU) = self._toGrid(vLU)
			(colC, rowC) = self._toGrid(vC)
			(colD, rowD) = self._toGrid(vRD)
			# read energy
			eLU = self._energy[self._height * colU + rowU]
			eC = self._energy[self._height * colC + rowC]
			eRD = self._energy[self._height * colD + rowD]
			
		else:
			# read energy directly from energy array
			eLU = self._energy[vLU]
			eC = self._energy[vC]
			eRD = self._energy[vRD]

		if eLU <= min(eC, eRD):
			self._edgeTo[v] = vLU
			self._distTo[v] = self._distTo[vLU] + eLU
		elif eRD <= min(eLU, eC):
			self._edgeTo[v] = vRD
			self._distTo[v] = self._distTo[vRD] + eRD
		else:
			self._edgeTo[v] = vC
			self._distTo[v] = self._distTo[vC] + eC




		

