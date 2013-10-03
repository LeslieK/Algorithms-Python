import argparse, png, array
from readPNG_2 import Picture
from SeamCarverLib import SeamCarver
import SeamCarverUtilities

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename of image", type=str)
parser.add_argument("rowsToRemove", help="number of rows to remove from image", type=int)
parser.add_argument("colsToRemove", help="number of cols to remove from image", type=int)
args = parser.parse_args()

print "build energy array for {}".format(args.filename)
pic = Picture(args.filename)

print "build graph of pixels from energy array"
sc = SeamCarver(pic)

#print pic.energyArray, '\nlen = ', len(pic.energyArray)

print "print vertical seam\n"
SeamCarverUtilities.printVerticalSeam(sc)
print "print horizontal seam\n"
SeamCarverUtilities.printHorizontalSeam(sc)


#print "remove {} rows".format(args.rowsToRemove)
#print "remove {} cols".format(args.colsToRemove)

