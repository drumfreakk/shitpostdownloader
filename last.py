import cv2
from imutils import paths
import time
import os
from shutil import copyfile

# grab the paths to both the haystack and needle images 
haystackPaths = list(paths.list_images("/home/kip/test/main/imgs/main/"))
needlePaths = list(paths.list_images("/home/kip/test/main/imgs/rest/"))

# grab the base subdirectories for the needle paths, initialize the
# dictionary that will map the image hash to corresponding image,
# hashes, then start the timer
newPics = []
haystack = {}
start = time.time()

def dhash(image, hashSize=8):
	# resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hashSize + 1, hashSize))
 
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
 
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def getImgHash(path):
	# load the image from disk
	image = cv2.imread(path)
 
	# if the image is None then we could not load it from disk (so
	# skip it)
	if image is None:
		return
 
	# convert the image to grayscale and compute the hash
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return dhash(image)

def addToHaystack(path):
	global haystack

	imageHash = getImgHash(path)
 
	# update the haystack dictionary
	l = haystack.get(imageHash, [])
	l.append(path)
	haystack[imageHash] = l

##-----------------INIT HAYSTACK---------------------##
# loop over the haystack paths
for p in haystackPaths:
	addToHaystack(p)

print haystack

# loop over the needle paths
for p in needlePaths:

	imageHash = getImgHash(p)
 
	# grab all image paths that match the hash
	matchedPaths = haystack.get(imageHash, [])
	print ' '
	print p
	print imageHash
	print matchedPaths

	# loop over all matched paths
	if matchedPaths == []:
		copyfile(p, p.replace("rest", "main"))
		addToHaystack(p.replace("rest", "main"))
		print haystack



