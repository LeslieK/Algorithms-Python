import png, array

def printVerticalSeam(sc):
	"vertical seam is a list of cols"
	seam = sc.findVerticalSeam()
	totalSeamEnergy = 0
	for row in range(sc.height()):
		for col in range(sc.width()):
			lmarker = ' '
			rmarker = ' '
			if col == seam[row]:
				lmarker = '['
				rmarker = ']'
				totalSeamEnergy += sc.energy(col, row)
			print '{:s}{:>6d}{:s}'.format(lmarker, sc.energy(col, row), rmarker),
		print
	print "\nTotal seam energy: {:d}".format(totalSeamEnergy)


def printHorizontalSeam(sc):
	"horizontal seam is a list of rows"
	seam = sc.findHorizontalSeam()
	totalSeamEnergy = 0
	for row in range(sc.height()):
		for col in range(sc.width()):
			lmarker = ' '
			rmarker = ' '
			if row == seam[col]:
				lmarker = '['
				rmarker = ']'
				totalSeamEnergy += sc.energy(col, row)
			print '{:s}{:>6d}{:s}'.format(lmarker, sc.energy(col, row), rmarker),
		print
	print "\nTotal seam energy: {:d}".format(totalSeamEnergy) 

def printVerticalSeamEnergy(sc):
	"vertical seam is a list of cols"
	seam = sc.findVerticalSeam()
	totalSeamEnergy = 0
	for row in range(sc.height()):
		for col in range(sc.width()):
			if col == seam[row]:
				totalSeamEnergy += sc.energy(col, row)
	print "\nTotal seam energy: {:d}".format(totalSeamEnergy)

def printHorizontalSeamEnergy(sc):
	"horizontal seam is a list of rows"
	seam = sc.findHorizontalSeam()
	totalSeamEnergy = 0
	for row in range(sc.height()):
		for col in range(sc.width()):
			if row == seam[col]:
				totalSeamEnergy += sc.energy(col, row)
	print "\nTotal seam energy: {:d}".format(totalSeamEnergy)


def distToArray(sc):
	"displays distTo in matrix format"
	print "sc._distTo array\n"
	for r in range(sc.height()):
		for c in range(sc.width()):
			print '{:>8d}'.format(sc._distTo[r * sc.width() + c]),
		print

def _normalize(data):
	"normalize values in data collection"
	maxVal = max(data)
	normal_data = map(lambda x: x/float(maxVal), data)
	return normal_data

def convertToGrayscale(sc, filename_out, seam=None, horizontal=True):
	"converts sc.energy array to png image of grayscale values"
	w = png.Writer(width=sc.width(), height=sc.height(), bitdepth=8, greyscale=True)
	normal_energy = [int(round(x * 255)) for x in _normalize(sc._energy)]
	if seam:
		# write energy png with seam overlay
		_RED = 255
		if horizontal:
			# horizontal seam
			for col, row in enumerate(seam):
				index = row * sc.width() + col
				normal_energy[index] = _RED
		else:
			# vertical seam
			for row, col in enumerate(seam):
				index = row * sc.width() + col
				normal_energy[index] = _RED
		# write png 
		
		with open(filename_out, 'wb') as f:
			w.write_array(f, normal_energy)









