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