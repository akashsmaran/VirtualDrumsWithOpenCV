from collections import deque
import numpy as np
import argparse
import imutils 
import cv2
import subprocess
from threading import Thread

def sound1():
	subprocess.call("python soundcheck2.py", shell=True)

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="path to the (optional) video file")
ap.add_argument("-b","--buffer",type = int, default = 32,help="max buffer size")
args = vars(ap.parse_args())
"""
greenLower = (26, 86, 6)
greenUpper = (36, 255, 255)

blue_lower=np.array([100,150,0],np.uint8)
blue_upper=np.array([140,255,255],np.uint8)
"""
blueLower = (100, 150, 0)
blueUpper = (140, 255, 255)

pts = deque(maxlen = args["buffer"])
counter = 0
(dX, dY) = (0, 0)
direction = ""
count = 0

if not args.get("video", False):
	camera = cv2.VideoCapture(0)

else: 
	camera = cv2.VideoCapture(args["video"])

while True:
	(grabbed, frame) = camera.read()
	
	if args.get("video") and not grabbed:
		break
	numFrameToSave = 3
	if (count % numFrameToSave ==0):
		frame = imutils.resize(frame, width=600)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		
		mask = cv2.inRange(hsv, blueLower, blueUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask,  None, iterations=2)

		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		#print(cnts)
		center = None
		key =0
		if len(cnts)>0:
			for c in cnts: 
			#c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			
				if radius > 10:
					cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
					pts.appendleft(center)
					counter = counter+1

				if(x>56 and x<220 and y>280 and y<395 and radius>10):
					bg_thread = Thread(target=sound1)
					bg_thread.start()	

			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF

		
		if key == ord("q"):
			break
	count += 1
	
	"""
	if len(cnts)>0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		
		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			pts.appendleft(center)
			counter = counter+1
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if key == ord("q"):
		break
	"""
camera.release()
cv2.destroyAllWindows()	
