import cv2
import sys

# edges detection treshold
canny_settings = [5, 100]
sourceFilePath = sys.argv[1]

image = cv2.imread(sourceFilePath)
_size = image.shape
#print(_size)
edged = cv2.Canny(image, canny_settings[0], canny_settings[1])

#applying closing function
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
#cv2.imwrite(resultFilePath + "_closed_" + add + ".jpg", closed)

#finding_contours
(_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

minX = None
minY = None
maxX = None
maxY = None
	
for c in cnts:
	x,y,w,h = cv2.boundingRect(c)		
	#cv2.rectangle(image, (x, y), (x + w, y + h), (0,255,0), 3);
	#print(w, h)
	
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

print(str(minX) + "," + str(minY) + "," + str(maxX) + "," + str(maxY))