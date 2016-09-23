import cv2
import os.path

while True:
	if os.path.exists("image.pgm"):
		image = cv2.imread("image.pgm")
		if not image is None and len(image) > 0:
			cv2.imshow("Frame", image)
			cv2.waitKey(20)