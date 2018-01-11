# USAGE
# python center_of_shape.py --image shapes_and_colors.png

# import the necessary packages
import argparse
import cv2
import numpy as np
import math
#import face_recognition
# import cv2
import numpy
#import queue as queue
#from threading import Thread
import time
import os

def scan(im_url, debug=True):
	
	#im_url = 'http://192.168.0.155:4747/mjpegfeed?960x720'
	#path = os.path.dirname(os.path.abspath(__file__))
	#im_url = os.path.join(path, '/CalibImg.jpg')
	#print(im_url)
	crop_topleft = (320, 0)
	crop_bottomright = (700, 720)

	boundaries = [
		(([190, 140, 70], [255, 230, 150]), "blue"),
		(([15, 190, 210], [90, 255, 255]), "yellow"),
		(([90, 90, 90], [150, 150, 150]), "grey"),
		(([200, 110, 150], [250, 180, 210]), "purple"),
		(([100, 170, 0], [150, 220, 100]), "green"),
		(([125, 80, 210], [200, 155, 255]), "pink"),
		(([25, 10, 150], [105, 110, 250]), "red"),
		
	]

	# defined in B G R

	color_def = [
		([35, 28, 233], "red"),
		([133, 226, 11], "green"),
		([255, 241, 127], "blue"),
		([82, 237, 253], "yellow"),
		([229, 168, 255], "pink"),
		([246, 178, 201], "purple"),
		([99, 212, 155], "leaf"),
		([210, 230, 231], "cream"),
	]


	camera = cv2.VideoCapture(im_url)
	_, non_crop_image = camera.read()
	for i in range(50):
		_, non_crop_image = camera.read()


	#non_crop_image = cv2.imread(im_url)

	#print(non_crop_image.shape)

	image = non_crop_image[crop_topleft[1]:crop_bottomright[1], crop_topleft[0]:crop_bottomright[0]]

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	black_lower = np.array([0, 0, 0])
	black_upper = np.array([179, 128, 128])
	mask = cv2.inRange(hsv, black_lower, black_upper)
	mask = cv2.bitwise_not(mask, mask)
	#cv2.imshow('mask', mask)
	#res = cv2.bitwise_and

	#gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
	gray = mask
	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	#blurred = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
	#blurred = cv2.bilateralFilter(gray, 9, 256, 256)

	thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

	# find contours in the thresholded image
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[1]# if imutils.is_cv2() else cnts[1]

	WEIGHTLIMIT = 2000.0

	allItems = []
	# loop over the contours
	for c in cnts:
		# compute the center of the contour
		M = cv2.moments(c)
		#print(M["m00"])
		if (M["m00"] <= WEIGHTLIMIT):
			pass
		else:
			cX = int(M["m10"] / M["m00"])
			cY = int(M["m01"] / M["m00"])
			
			u11 = M["mu11"];
			u02 = M["mu02"];
			u20 = M["mu20"];
			radian = math.atan2(-2.0*u11, u20 - u02 ) / 2.0;
			angle = 90.0 + 90.0 - radian * (180.0/3.14159265359);

			color = image[cY, cX]
			
			#print(color)

			min_d = 500.0
			name = 'none'
			
			for (c_val, c_name) in color_def:
				d = compare_color(color, c_val)
				#print(c_val)
				if d < min_d:
					min_d = d
					name = c_name
			cv2.putText(image, name, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

			'''
			for (bound, name) in boundaries:
				lower = np.array(bound[0], dtype = "uint8")
				upper = np.array(bound[1], dtype = "uint8")
				print((np.greater_equal(color, lower)))
				if np.all((np.greater_equal(color, lower))) and np.all((np.greater_equal(upper, color))):
					cv2.putText(image, name, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
			'''
			# draw the contour and center of the shape on the image
			cv2.drawContours(image, [c], -1, (255, 255, 255), 2)
			length = 200.0
			
			image = cv2.line(image,(int(cX - length * math.cos(angle * np.pi / 180.0)),int(cY - length * math.sin(angle * np.pi / 180.0))),(int(cX + length * math.cos(angle * np.pi / 180.0)),int(cY + length * math.sin(angle * np.pi / 180.0))),(0,255,0),1)

			allItems.append({"center": (cX+crop_topleft[0], cY+crop_topleft[1]), "degree": angle, "color": name})
	
	if debug:
		# show the image

		cv2.imshow("Blurred", blurred)
		cv2.waitKey(0)
		cv2.imshow("Thresholded", thresh)
		cv2.waitKey(0)
		cv2.imshow("Segmented", image)
		cv2.waitKey(0)

	return allItems

def compare_color(c1, c2):
	db = abs(c1[0] - c2[0])
	dg = abs(c1[1] - c2[1])
	dr = abs(c1[2] - c2[2])
	return math.sqrt((db ** 2) + (dg ** 2) + (dr ** 2))

#print(cam_scan())