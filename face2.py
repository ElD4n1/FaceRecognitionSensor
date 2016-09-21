import numpy as np
import cv2

video = "/dev/video0"
video_capture = cv2.VideoCapture(video)

while True:
	ret, frame = video_capture.read()
	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
cv2.destroyAllWindows()
