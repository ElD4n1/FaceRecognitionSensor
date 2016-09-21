import cv2
import threading
import v4l2capture
import imutils
import time
import numpy as np

def detect_faces(image):
	haar_cascade = cv2.CascadeClassifier()
	haar_cascade.load('haarcascade_frontalface_default.xml')
	faces = haar_cascade.detectMultiScale(image)
	return faces
		
class FaceVideoStreamFrame(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.isRunning = False
		video = "/dev/video0"
		self.video_capture = cv2.VideoCapture(video)
		self.lock = threading.Lock()

	def run(self):
		# initialize the video stream and allow the cammera sensor to warmup
		time.sleep(2.0)
		self.isRunning = True
		# loop over the frames from the video stream
		while self.isRunning:
			# grab the frame from the threaded video stream and resize it
			# to have a maximum width of 400 pixels
			self.lock.acquire()
			ret, frame = self.video_capture.read()
			self.currentFrame = frame
			self.lock.release()

			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			faces = detect_faces(gray)

			# Draw a rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

			frame = imutils.resize(frame, width=400)
			# show the frame
			cv2.imshow("Frame", frame)
			
			#self.stream.truncate(0) #Must use this to eliminate the error: "Incorrect buffer length"
			
			key = cv2.waitKey(10) & 0xFF
		cv2.destroyAllWindows()

	def stop(self):
		self.isRunning = False
		self.video_capture.release()
		print("VideoStream stopped, all resources freed")

	def getCurrentFrame(self):
		if(not self.isRunning):
			time.sleep(2.1)
		if(self.isRunning):
			#return self.vs.read()
			#return self.stream.array
			self.lock.acquire()
			result = np.array(self.currentFrame)
			self.lock.release()
			return self.currentFrame
			
