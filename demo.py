import cv2
import numpy as np
import uuid

im = cv2.imread("test.jpg")
print(im.shape)
print(im[0,0])
print(im[0,0][0])
print(im[0,0][1])
print(im[0,0][2])

x1 = None
y1 = None
x2 = None
y2 = None
backgroundBgr = [255, 255, 255]

for y in range(0, im.shape[0] - 1):
	#print(y)
	for x in range(0, im.shape[1] - 1):
		#print(x)
		bgr = im[y, x]
		for i,v in enumerate(bgr):			
			if abs(v - backgroundBgr[i]) > 10:
				if (x1 is None) or (x < x1):
					x1 = x
				if (x2 is None) or (x > x2):
					x2 = x
				if (y1 is None) or (y < y1):
					y1 = y
				if (y2 is None) or (y > y2):
					y2 = y
				break;

print(x1, y1, x2, y2)

cv2.rectangle(im, (x1, y1), (x2, y2), (0,0,255), 3);
cv2.imwrite(str(uuid.uuid4()) + ".jpg", im)

	
# bgr
'''
cv2.rectangle(im, (10, 10), (20, 20), (0,0,255));

im2 = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

cv2.imshow("Over the Clouds", im)
cv2.imshow("Over the Clouds - gray", im2)

cv2.waitKey(0)
cv2.destroyAllWindows()
'''
