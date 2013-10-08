from decimal import Decimal
_INF = Decimal('infinity')
_SENTINEL = -1
#_BORDER_ENERGY = 195075
_BORDER_ENERGY = 195705
import pdb

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
		# self._edgeTo = [_SENTINEL for _ in range(self._num_pixels + 2)]	# add 2 for source, sink pixels
		# self._distTo = [_INF for _ in range(self._num_pixels + 2)]
		self._edgeTo = []
		self._distTo = []


	def width(self):
		return self._width

	def height(self):
		return self._height

	def energy(self, col, row):
		"return energy of pixel in (col, row)"
		if self._isValid(col, row):
			return self._energy[self._toLinear(col, row)]

	def findVerticalSeam(self, transposed=False):
		"return vertical seam in image"
		# vertical seam = sequence of cols; seam[0] is col of row 0
		# row-indexed seam
		seam = [-1 for _ in range(self._height)]
		self._buildGraph(transposed)
		row = self._height - 1
		v = self._edgeTo[self._sink]
		while (v != self._source):
			seam[row] = v % self._width  # seam[row] = col
			v = self._edgeTo[v]
			row -= 1
		#self._edgeTo = []
		#self._distTo = []
		return seam

	def findHorizontalSeam(self, transposed=True):
		"return horizontal seam in image"
		# tranpose dimensions
		self._exchDims()

		# horizontal seam = sequence of rows; seam[0] is row of col 0
		# col-indexed seam
		seam = self.findVerticalSeam(transposed)
		self._exchDims()
		#self._edgeTo = []
		#self._distTo = []
		return seam

	def _shiftImgUp(self, (col, row)):
		"remove horizontal seam in img and energy array by shifting up each col"
		for r in range(row, self._height - 1):
			i = self._width * r + col
			rchan_index = i*3
			self._img[rchan_index] = self._img[rchan_index + self._width*3]
			self._img[rchan_index + 1] = self._img[rchan_index + 1 + self._width*3]
			self._img[rchan_index + 2] = self._img[rchan_index + 2 + self._width*3]
			self._energy[i] = self._energy[i + self._width]

	def _removeSeam(self, seam):
		"remove seam of pixels from image"
		# remove horizontal seam
		if(len(seam)) != self._width or self._width < 2:
			raise ValueError
		#indexes_to_remove = map(lambda (col, r): self._width * r + col, enumerate(seam))
		# remove seam pixels from image
		map(self._shiftImgUp, [t for t in enumerate(seam)])
		self._height -= 1
		self._num_pixels = self._width * self._height
		self._source = self._num_pixels
		self._sink = self._source + 1


	def removeVerticalSeam(self, seam):
		"remove vertical seam of pixels from image"
		if (len(seam) != self._height or self._height == 0 or self._width == 2):
			raise ValueError
		indexes_to_remove = map(lambda (r, col): self._width * r + col, enumerate(seam))
		
		# img array ; each pixel is represented by 3 or 4 unsigned integers
		R_chan =  map(lambda x: x * self._num_channels, indexes_to_remove)
		G_chan = map(lambda x: x + 1, R_chan)
		B_chan = map(lambda x: x + 2, R_chan)

		# make one list
		pixels_to_remove = []
		pixels_to_remove.extend(R_chan)
		pixels_to_remove.extend(G_chan)
		pixels_to_remove.extend(B_chan)
		if self._num_channels == 4:
			alpha_chan = map(lambda x: x + 3, R_chan)
			pixels_to_remove.extend(alpha_chan)

		# remove energy values associated with removed pixels
		self._energy = map(lambda (x, y): y, filter(lambda (x, y): x not in indexes_to_remove, enumerate(self._energy)))

		# remove seam pixels from image
		self._img = map(lambda (x, y): y, filter(lambda (x, y): x not in pixels_to_remove, enumerate(self._img)))
		resized_width = self._width - 1
		resized_num_pix = resized_width * self._height

		# update energy array
		self._updateEnergy(R_chan, resized_width)
		
		# update image dimension, number of pixels
		self._width = resized_width
		self._num_pixels = resized_num_pix
		self._source = self._num_pixels
		self._sink = self._source + 1
	
	def removeHorizontalSeam(self, seam):
		"remove horizontal seam of pixels"
		self._removeSeam(seam)

		# update energy
		for col, row in enumerate(seam):
			index = self._width * row + col
			if row == self._height - 1:
				# index on bottom edge; row above bottom edge becomes border
				self._energy[index - self._width] = _BORDER_ENERGY
			elif not self._onEdge:
				# index is not on boundary
				# update energy of pixel in seam position
				self._energyGrad(index, self._width, transposed=False)	
				if row > 1:
					# update energy of pixel above seam position
					self._energyGrad(index - self._width, self._width, transposed=False)
					

	def _onEdge(self, col, row):
		"True if pixel is on left, top, or right edge"
		return col == 0 or col == self._width - 1 or row == 0

	def _updateEnergy(self, R_chan, resized_width):
		'''re-calculate energy values for pixels on either side of seam

		R_chan is a list of R channels'''
		for R in R_chan:
			# index = index of seam pixel wrt original image
			index = R / self._num_channels
			col, row = self._toGrid(index)
			# col, row of seam pixel wrt original image
			# resized_index = index of pixel on right of seam in resized image

			resized_index = index - row


			# is seam pixel on a border of original image?
			if col == self._width - 1:
				# seam pixel is on right edge of original image
				# pixel on left of seam pixel is border in resized image
				self._energy[index - row - 1] = _BORDER_ENERGY
				continue
			elif (col == 0):
				# seam pixel on left edge of original image
				self._energy[index - row] = _BORDER_ENERGY
				continue
			elif (row == 0):
				# seam pixel on top edge of original image
				self._energy[index] = _BORDER_ENERGY
				continue
			elif (row == self._height - 1):
				# seam pixel on bottom edge of original image
				self._energy[index - row] = _BORDER_ENERGY
				continue
			else:
				# pixel is not on a border of original image
				# there is a new pixel in position resized_index (index wrt resized image); shifted in from the right

				if (resized_index % resized_width == resized_width - 1):
				# resized_index is on right border of resized img	
					self._energy[resized_index] = _BORDER_ENERGY
				else:
					# resized_index refers to an inner pixel in resized image	
					self._energyGrad(resized_index, resized_width)
				if ((resized_index - 1) % resized_width) == 0:
					# pixel to left of seam is on left edge
					self._energy[resized_index - 1] = _BORDER_ENERGY
				else:
					self._energyGrad(resized_index - 1, resized_width)
			
	def _energyGrad(self, index, width):
		'''Calculate energy of pixel in resized image. Update self._energy

		uses resized_index and resized_width'''

		left = (index  - 1) * self._num_channels
		right = (index + 1) * self._num_channels

		RL = self._img[left]
		GL = self._img[left + 1]
		BL = self._img[left + 2]
		RR = self._img[right]
		GR = self._img[right + 1]
		BR = self._img[right + 2]
		gradH = self._diff_squared(RL, RR) + self._diff_squared(GL, GR) + self._diff_squared(BL, BR)

		up = (index  - width) * self._num_channels
		down = (index + width) * self._num_channels

		RU = self._img[up]
		GU = self._img[up + 1]
		BU = self._img[up + 2]
		RD = self._img[down]
		GD = self._img[down + 1]
		BD = self._img[down + 2]
		gradV = self._diff_squared(RU, RD) + self._diff_squared(GU, GD) + self._diff_squared(BU, BD)

		self._energy[index] = gradH + gradV

	def _diff_squared(self, x, y):
		return (x - y)**2

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

	def _buildGraph(self, transposed):
		"pixels are nodes; edges define precedence constraints in a seam"
		# graph data structures
		self._edgeTo = [_SENTINEL for _ in range(self._num_pixels + 2)]	# add 2 for source, sink pixels
		self._distTo = [_INF for _ in range(self._num_pixels + 2)]
		
		# for row 0 pixels: distTo[] is 0; edgeTo[] is _source vertex 
		for i in range(0, self._width):
			self._distTo[i] = 0
			self._edgeTo[i] = self._source
		# distTo[] is 0 for source pixel
		self._distTo[self._source] = 0

		# for each vertex (pixel), calculate edgeTo[], distTo[]
		# start at row 1
		for v in range(self._width, self._num_pixels):
			if (v % self._width == 0):
				# pixel is on left edge
				self._edgeTodistTo(v, transposed, edgeL=True)
			elif (v % self._width == self._width - 1):
				# pixel is on right edge
				self._edgeTodistTo(v, transposed, edgeR=True)
			else:
				self._edgeTodistTo(v, transposed)
		# edgeTo[sink] is vertex in last row with min energy
		index, min_energy = min(enumerate(self._distTo[self._num_pixels - self._width:self._num_pixels]), key=lambda (x, y): y)
		self._distTo[self._sink] = min_energy
		self._edgeTo[self._sink] = (self._height - 1) * self._width + index



	def _edgeTodistTo(self, v, transposed, edgeL=False, edgeR=False):
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
			#print (eLU, vLU), (eC, vC), (eRD, vRD)
		# find min distance and its associated vertex
		dist, from_vertex = min((self._distTo[vLU] + eLU, vLU), (self._distTo[vC] + eC, vC), (self._distTo[vRD] + eRD, vRD))
		#e, vertex = min([(eC, vC), (eLU, vLU), (eRD, vRD)])
		self._edgeTo[v] = from_vertex
		self._distTo[v] = dist





		

