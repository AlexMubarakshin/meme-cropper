import numpy as np
import cv2
import time

im = 'img0.jpg'

im = cv2.imread(im)

# Some content_images share the same border as the image itself.
# In this case, the correct contour is not found. We add a white
# border around the image to fix this. 
def addWhiteBorder(im):
	#TODO 
	return null

def getContours(im):
	imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	imgray = cv2.bilateralFilter(imgray, 11, 17, 17)
	ret, thresh = cv2.threshold(imgray, 240, 240, 0)
	im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours

def getImageContour(contours):
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
	image_contour = None
	count = 0
	for contour in contours:
		peri = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

		if len(approx) == 4:
			image_contour = approx
			count = count + 1
			if count > 1:
				print image_contour
				break

	return image_contour

def saveCroppedImage(im, image_contour):
	cv2.drawContours(im, [screen_contour], -1, (255,255,0), 3)
	cv2.imwrite('im_with_contour.jpg',im)

	y0 = min(screen_contour[0][0][1],screen_contour[1][0][1],screen_contour[2][0][1],screen_contour[3][0][1])
	y1 = max(screen_contour[0][0][1],screen_contour[1][0][1],screen_contour[2][0][1],screen_contour[3][0][1])

	x0 = min(screen_contour[0][0][0],screen_contour[1][0][0],screen_contour[2][0][0],screen_contour[3][0][0])
	x1 = max(screen_contour[0][0][0],screen_contour[1][0][0],screen_contour[2][0][0],screen_contour[3][0][0])
	print y0,y1,x0,x1
	im_cropped = im[y0:y1, x0:x1]
	cv2.imwrite('im_cropped.jpg',im_cropped)

imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
imgray = cv2.bilateralFilter(imgray, 11, 17, 17)

#1
# edged = cv2.Canny(imgray, 30, 200)
#2
ret, thresh = cv2.threshold(imgray, 240, 240, 0)

#1
# im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#2
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

screen_contour = None

count = 0
for contour in contours:
	peri = cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

	if len(approx) == 4:
		screen_contour = approx
		count = count + 1
		if count > 1:
			print screen_contour
			break

# show the screen_contour on the image
cv2.drawContours(im, [screen_contour], -1, (255,255,0), 3)


cv2.imwrite('im_with_contour.jpg',im)

y0 = min(screen_contour[0][0][1],screen_contour[1][0][1],screen_contour[2][0][1],screen_contour[3][0][1])
y1 = max(screen_contour[0][0][1],screen_contour[1][0][1],screen_contour[2][0][1],screen_contour[3][0][1])

x0 = min(screen_contour[0][0][0],screen_contour[1][0][0],screen_contour[2][0][0],screen_contour[3][0][0])
x1 = max(screen_contour[0][0][0],screen_contour[1][0][0],screen_contour[2][0][0],screen_contour[3][0][0])

print y0,y1,x0,x1

im_cropped = im[y0:y1, x0:x1]

cv2.imwrite('im_cropped.jpg',im_cropped)


# cv2.imshow("cropped", imgray)
# cv2.waitKey(0)