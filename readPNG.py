import png, array

_BORDER_ENERGY = 195075
_CH = 3		# number of channels (R,G,B = 3; R,G,B,A = 4)

r = png.Reader(filename='5x6.png')
res = r.read()
# res = (width, height, iterator-over-pixels, 
# 	    {'alpha': False, 'bitdepth': 8, greyscale': True,
#        'interlace': 0, 'planes': 1, size':(255, 1)})

num_cols = res[0]
num_rows = res[1]
if res[3]['alpha']:
	_CH = 4

def diff_squared(x, y):
	return (x-y)**2

energyArray = array.array("L")
# top row of energy array
energyArray.extend([_BORDER_ENERGY] * num_cols)

# row 0 of image
row_prev = res[2].next()

# find energy of row 1
row_curr = res[2].next()

for row_next in res[2]:
	"build energy array of image"

	# calculate gradient of current row
	gradRv = map(diff_squared, row_prev[0::_CH], row_next[0::_CH])
	gradGv = map(diff_squared, row_prev[1::_CH], row_next[1::_CH])
	gradBv = map(diff_squared, row_prev[2::_CH], row_next[2::_CH])
	n = num_cols * _CH
	gradRh = map(diff_squared, row_curr[0:(n - 2*_CH):_CH], row_curr[2*_CH:(n - _CH)+1:_CH])
	gradGh = map(diff_squared, row_curr[1:(n - 2*_CH):_CH], row_curr[2*_CH+1:(n - _CH)+2:_CH])
	gradBh = map(diff_squared, row_curr[2:(n - 2*_CH):_CH], row_curr[2*_CH+2:(n - _CH)+3:_CH])

	gradR = map(int.__add__, gradRv[1:-1], gradRh)
	gradG = map(int.__add__, gradGv[1:-1], gradGh)
	gradB = map(int.__add__, gradBv[1:-1], gradBh)

	# calculate energy of current row
	energy = map(sum, zip(gradR, gradG, gradB))

	# left border pixel energy 
	energyArray.append(_BORDER_ENERGY)
	# non-border pixel energy
	energyArray.extend(energy)
	# right border pixel energy
	energyArray.append(_BORDER_ENERGY)

	row_prev = row_curr
	row_curr = row_next

# bottom row of energy array
energyArray.extend([_BORDER_ENERGY] * num_cols)




