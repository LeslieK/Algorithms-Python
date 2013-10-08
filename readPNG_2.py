import png, array


class Picture(object):
	"reads a png image from a filename"
	#BORDER_ENERGY = 195075
	BORDER_ENERGY = 195705
	
	
	def __init__(self, pngfilename):
		"reads in a .png image"
		_CH = 3		# number of channels (R,G,B = 3; R,G,B,A = 4)
		_r = png.Reader(filename=pngfilename)
		res = _r.read()
	# 	res = (width, height, iterator-over-pixels, 
	# 	    	{'alpha': False, 'bitdepth': 8, greyscale': True,
	#        	'interlace': 0, 'planes': 1, size':(255, 1)})

		self.num_cols = res[0]
		self.num_rows = res[1]

		if res[3]['alpha']:
			_CH = 4

		self.num_channels = _CH

		self.energyArray = array.array("L")
		self.imageArray = array.array("B")
		
		# row 0 of image
		_row_prev = res[2].next()
		self.energyArray.extend([Picture.BORDER_ENERGY] * self.num_cols)
		self.imageArray.extend(_row_prev)

		if (self.num_rows == 1):
			return

		# row 1 of image
		_row_curr = res[2].next()
		self.imageArray.extend(_row_curr)
		if (self.num_rows == 2):
			self.energyArray.extend([Picture.BORDER_ENERGY] * self.num_cols)
			return
		
		# for images with more than 2 rows
		for _row_next in res[2]:
			"build image array and energy array"

			# add _row_next to image array
			self.imageArray.extend(_row_next)

			# calculate gradient of current row
			_gradRv = map(self._diff_squared, _row_prev[0::_CH], _row_next[0::_CH])
			_gradGv = map(self._diff_squared, _row_prev[1::_CH], _row_next[1::_CH])
			_gradBv = map(self._diff_squared, _row_prev[2::_CH], _row_next[2::_CH])
			n = self.num_cols * _CH
			_gradRh = map(self._diff_squared, _row_curr[0:(n - 2*_CH):_CH], _row_curr[2*_CH:(n - _CH)+1:_CH])
			_gradGh = map(self._diff_squared, _row_curr[1:(n - 2*_CH):_CH], _row_curr[2*_CH+1:(n - _CH)+2:_CH])
			_gradBh = map(self._diff_squared, _row_curr[2:(n - 2*_CH):_CH], _row_curr[2*_CH+2:(n - _CH)+3:_CH])

			_gradR = map(int.__add__, _gradRv[1:-1], _gradRh)
			_gradG = map(int.__add__, _gradGv[1:-1], _gradGh)
			_gradB = map(int.__add__, _gradBv[1:-1], _gradBh)

			# calculate energy of current row
			_energy = map(sum, zip(_gradR, _gradG, _gradB))

			# left border pixel energy 
			self.energyArray.append(Picture.BORDER_ENERGY)
			# non-border pixel energy
			self.energyArray.extend(_energy)
			# right border pixel energy
			self.energyArray.append(Picture.BORDER_ENERGY)

			_row_prev = _row_curr
			_row_curr = _row_next

		# bottom row of energy array
		print 'i am in Picture'
		self.energyArray.extend([Picture.BORDER_ENERGY] * self.num_cols)


	def _diff_squared(self, x, y):
		return (x-y)**2

