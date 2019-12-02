import cv2
from imutils import paths
import argparse
import time
import os

vidcap = cv2.VideoCapture('yt.mp4')
success,image = vidcap.read()
count = 0
while success:
	cv2.imwrite("imgs/rest/frame%d.jpg" % count, image)     # save frame as JPEG file      
	success,image = vidcap.read()
	print('Read a new frame: ', success)
	count += 1
