# USAGE
# python center_of_shape.py --image shapes_and_colors.png

# import the necessary packages
import argparse
import cv2
import numpy as np
import math
import face_recognition
import cv2
import numpy
import queue as queue
from threading import Thread
import time
boundaries = [
	(([200, 150, 70], [255, 220, 140]), "blue"),
	(([50, 200, 220], [100, 255, 255]), "yellow"),
	(([100, 100, 100], [150, 150, 150]), "grey"),
	(([210, 120, 160], [250, 170, 200]), "purple"),
	(([100, 160, 50], [140, 210, 90]), "green"),
	(([135, 90, 220], [190, 145, 255]), "pink"),
	(([35, 45, 160], [95, 100, 220]), "red"),
	
]

def do_stuff():
	while True:
		# construct the argument parse and parse the arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-i", "--image", required=True,
			help="path to the input image")
		args = vars(ap.parse_args())

		# load the image, convert it to grayscale, blur it slightly,
		# and threshold it
		image = cv2.VideoCapture(0)
	#	image = cv2.imread(args["image"])
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

		# find contours in the thresholded image
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[1]# if imutils.is_cv2() else cnts[1]

		WEIGHTLIMIT = 10000.0

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
				cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
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
			
		
		
	# show the image
#	cv2.imshow("Image", image)
#	cv2.waitKey(0)
	

worker = Thread(target=do_stuff, args=())
worker.setDaemon(True)
worker.start()
worker.join()