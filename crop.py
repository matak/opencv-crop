import os
import cv2
import sys
import numpy as np
import pprint

#canny_settings = [5, 250]
#stick_canny_settings = [5, 100]
canny_settings = [5, 100]
stype = ""
#stype = "_test"
sourcePath = "./sources" + stype
resultPath = "./result" + stype + "_" + str(canny_settings[0]) + "-" + str(canny_settings[1])

if not os.path.exists(resultPath):
	os.makedirs(resultPath)
	
def findStickMinY( closedImage ):
	rows = closedImage.shape[0] - 1;
	cols = closedImage.shape[1] - 1;
	pole_width = 100
	pole_height = 50
	pole_line_counter = 0
	pole_found = 0
	
	for y in range(0, rows):
		line = rows - y
		#print(y)
		minX = None
		maxX = None
		
		for x in range(0, cols):
			#print(x)
			#print(closedImage[line, x])
			if closedImage[line, x] == 255:
				if (minX is None) or (x < minX):
					minX = x
				if (maxX is None) or (x > maxX):
					maxX = x
					
		if pole_found == 0:
			if (minX is not None) and (maxX is not None) and (maxX - minX < pole_width):
				pole_line_counter += 1
			else:
				pole_line_counter = 0			

			if pole_line_counter == pole_height:
				pole_found = 1
				
		else:
			if (minX is not None) and (maxX is not None) and (maxX - minX > pole_width):
				break
			
	return line

def process( resultPath, filePath ):
	resultFilePath = resultPath + "/" + os.path.basename(filePath)
	add = "1"
	
	#reading the image
	image = cv2.imread(filePath)
	_size = image.shape
	print(_size)
	edged = cv2.Canny(image, canny_settings[0], canny_settings[1])
	#cv2.imwrite(resultFilePath + "_edges_" + add + ".jpg", edged)

	#applying closing function
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
	closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
	cv2.imwrite(resultFilePath + "_closed_" + add + ".jpg", closed)

	#finding_contours
	(_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	minX = None
	minY = None
	maxX = None
	maxY = None
	
	for c in cnts:
		x,y,w,h = cv2.boundingRect(c)		
		cv2.rectangle(image, (x, y), (x + w, y + h), (0,255,0), 3);
		print(w, h)
		#skip contours smaller then 1/100 of picture size
		if (w < _size[1] / 90) and (w < _size[0] / 90):
			continue		
		
		if (minX is None) or (x < minX):
			minX = x
			
		if (minY is None) or (y < minY):
			minY = y
			
		if (maxX is None) or (x + w) > maxX:
			maxX = x + w
			
		if (maxY is None) or (y + h) > maxY:
			maxY = y + h

	cv2.rectangle(image, (minX, minY), (maxX, maxY), (0,0,255), 3);
	cv2.imwrite(resultFilePath + "_output_" + add + ".jpg", image)
	
	stickY = findStickMinY(closed.copy())
	if stickY:
		cv2.rectangle(image, (minX, minY), (maxX, stickY), (255,0,0), 3);
		cv2.imwrite(resultFilePath + "_output_" + add + "_stick.jpg", image)		
		
	return

for filename in os.listdir(sourcePath):
    if filename.endswith(".jpg"): 
	    process(resultPath, sourcePath + "/" + filename)

