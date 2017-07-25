from PIL import Image
import numpy
import cv2
import time

# Some input images will not have a white border, which will mess up the search
# for the Twitter pic contour. We add a white border to every image so that the 
# second largest rectangular contour will always be the Twitter pic.	
def addWhiteBorder(im_naked):
	naked_size = im_naked.size
	bordered_size = (800, 800)
	im_bordered = Image.new("RGB", bordered_size, color = (255,255,255))
	im_bordered.paste(im_naked, ((bordered_size[0]-naked_size[0])/2,
	                      (bordered_size[1]-naked_size[1])/2))
	return im_bordered

# Use OpenCV to find the contours of the input image.s
def getContours(im):
	im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	im_gray = cv2.bilateralFilter(im_gray, 11, 17, 17)
	ret, thresh = cv2.threshold(im_gray, 240, 240, 0)
	im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours

# Select the second largest rectangular contour, this is the contour
# of the Twitter pic
def getPicContour(contours):
	contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
	pic_contour = None
	count = 0
	for contour in contours:
		peri = cv2.arcLength(contour, True)
		approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
		if len(approx) == 4:
			pic_contour = approx
			count = count + 1
			if count > 1:
				break
	return pic_contour

# Selects the min, max pair of coords for the Twitter pic's height and width
def getContourCoords(pic_contour):
	y0 = min(pic_contour[0][0][1],pic_contour[1][0][1],pic_contour[2][0][1],pic_contour[3][0][1])
	y1 = max(pic_contour[0][0][1],pic_contour[1][0][1],pic_contour[2][0][1],pic_contour[3][0][1])
	x0 = min(pic_contour[0][0][0],pic_contour[1][0][0],pic_contour[2][0][0],pic_contour[3][0][0])
	x1 = max(pic_contour[0][0][0],pic_contour[1][0][0],pic_contour[2][0][0],pic_contour[3][0][0])
	return (y0,y1,x0,x1)

# Crop the input image around the Twitter pic contour, and save the cropped image
def saveCroppedImage(im, pic_contour):
	(y0,y1,x0,x1) = getContourCoords(pic_contour)
	im_cropped = im[y0:y1, x0:x1]
	cv2.imwrite('im_cropped.jpg',im_cropped)

# converts PIL image format to OpenCV format
def convertPILtoOpenCV(im):
	open_cv_image = numpy.array(im)[:, :, ::-1].copy()
	return open_cv_image

def main():
	# im_path = 'img7.jpg'
	im_path = raw_input("Image to crop: ")
	im_naked = Image.open(im_path)
	im_bordered = addWhiteBorder(im_naked)
	im = convertPILtoOpenCV(im_bordered)
	contours = getContours(im)
	pic_contour = getPicContour(contours)
	saveCroppedImage(im, pic_contour)

main()
