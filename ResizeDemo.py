import argparse, png, array
from readPNG_2 import Picture
#from SeamCarverLib import SeamCarver
import SeamCarverLib
import SeamCarverUtilities
import pdb

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename of image", type=str)
parser.add_argument("rowsToRemove", help="number of rows to remove from image", type=int)
parser.add_argument("colsToRemove", help="number of cols to remove from image", type=int)
args = parser.parse_args()

print "build energy array for {}".format(args.filename)
pic = Picture(args.filename)

print "build graph of pixels from energy array"
sc = SeamCarverLib.SeamCarver(pic)

print "print vertical seam 1\n"
SeamCarverUtilities.printVerticalSeam(sc) 			# find 1st: good

print "print vertical seam 2"
s = sc.findVerticalSeam()
sc.removeVerticalSeam(s)  							# remove vert #1		
SeamCarverUtilities.printVerticalSeam(sc) 			# good

print "print vertical seam 3"
print sc.height(), sc.width()
s = sc.findVerticalSeam()							# find 2nd: good
sc.removeVerticalSeam(s) 							# remove vert #2					
#pdb.set_trace()
SeamCarverUtilities.printVerticalSeam(sc) 			# energy array: good; seam: bad

print "remove vertical seam 4"
s = sc.findVerticalSeam()
sc.removeVerticalSeam(s)
SeamCarverUtilities.printVerticalSeam(sc)


#print "remove {} rows".format(args.rowsToRemove)
#print "remove {} cols".format(args.colsToRemove)

