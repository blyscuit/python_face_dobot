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
import queue as queue
from threading import Thread
import time


def cam_scan():
	
	#im_url = 'http://192.168.0.155:4747/mjpegfeed?960x720'
	im_url = 'CalibImg.jpg'
	crop_topleft = (320, 0)
	crop_bottomright = (640, 720)

	boundaries = [
		(([190, 140, 70], [255, 230, 150]), "blue"),
		(([15, 190, 210], [90, 255, 255]), "yellow"),
		(([90, 90, 90], [150, 150, 150]), "grey"),
		(([200, 110, 150], [250, 180, 210]), "purple"),
		(([100, 170, 0], [150, 220, 100]), "green"),
		(([125, 80, 210], [200, 155, 255]), "pink"),
		(([25, 10, 150], [105, 110, 250]), "red"),
		
	]

	'''
	camera = cv2.VideoCapture(im_url)
	_, non_crop_image = camera.read()
	for i in range(20):
		_, non_crop_image = camera.read()
	'''
	non_crop_image = cv2.imread(im_url)
	image = non_crop_image[crop_topleft[1]:crop_bottomright[1], crop_topleft[0]:crop_bottomright[0]]
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	blurred = cv2.bilateralFilter(gray, 9, 150, 150)

	cv2.imshow("Image", blurred)
	cv2.waitKey(0)

	thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

	cv2.imshow("Image", thresh)
	cv2.waitKey(0)

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
		print(M["m00"])
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
			
			print(color)
			
			for (bound, name) in boundaries:
				lower = np.array(bound[0], dtype = "uint8")
				upper = np.array(bound[1], dtype = "uint8")
		#		print((np.greater_equal(color, lower)))
				if np.all((np.greater_equal(color, lower))) and np.all((np.greater_equal(upper, color))):
					cv2.putText(image, name, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
			# draw the contour and center of the shape on the image
			cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			# cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)

			cv2.circle(image, (cX+crop_topleft[0], cY+crop_topleft[1]), 7, (255, 255, 255), -1)
			cv2.circle(image, (int(960/2), int(720/2)), 7, (255,255,0), -1)
		#	cv2.putText(image, "center", (cX - 20, cY - 20),
		#		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
			
		#	print(str(cX) + " " + str(cY))
			
		#	minRect = cv2.minAreaRect(c)
			
		#	print (angle)

		#	angle = minRect[2]
		#	
		#	θ = angle * 3.14 / 180.0
			length = 200.0
			
			image = cv2.line(image,(int(cX - length * math.cos(angle * np.pi / 180.0)),int(cY - length * math.sin(angle * np.pi / 180.0))),(int(cX + length * math.cos(angle * np.pi / 180.0)),int(cY + length * math.sin(angle * np.pi / 180.0))),(0,255,0),1)

			allItems.append({"center": (cX+crop_topleft[0], cY+crop_topleft[1]), "degree": angle, "color": name})
			# show the image
			cv2.imshow("Image", image)
			cv2.waitKey(0)

	return allItems

print(cam_scan())