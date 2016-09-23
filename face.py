import cv2
import threading
import v4l2capture
import imutils
import time
import numpy as np
import subprocess
import os

def detect_faces(image):
	haar_cascade = cv2.CascadeClassifier()
	haar_cascade.load('haarcascade_frontalface_default.xml')
	faces = haar_cascade.detectMultiScale(image)
	return faces
		
class FaceVideoStreamFrame(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.isRunning = False
		# load the video driver module
		subprocess.call(['sudo', 'modprobe', 'bcm2835-v4l2'])
		video = "/dev/video0"
		self.video_capture = cv2.VideoCapture(video)
		#self.video_capture.set(3,1920)
		#self.video_capture.set(4,1080)
		self.faces = []
		#self.lock = threading.Lock()
		#os.system("python3 imshow.py")
		subprocess.Popen(["python3", "imshow.py"])
		
	def run(self):
		# initialize the video stream and allow the cammera sensor to warmup
		#time.sleep(2.0)
		self.isRunning = True
		#cv2.startWindowThread()
		#cv2.namedWindow("Frame")
		# loop over the frames from the video stream
		while self.isRunning:
			# grab the frame from the threaded video stream and resize it
			# to have a maximum width of 400 pixels
			#self.lock.acquire()
			ret, self.currentFrame = self.video_capture.read()
			#self.lock.release()

			gray = cv2.cvtColor(self.currentFrame, cv2.COLOR_BGR2GRAY)
			self.currentGray = gray

			self.faces = detect_faces(gray)

			# Draw a rectangle around the faces
			for (x, y, w, h) in self.faces:
				cv2.rectangle(self.currentFrame, (x,y), (x+w, y+h), (255,0,0), 2)

			#frame = imutils.resize(frame, width=400)
			# show the frame
			#print("showing the frame")
			cv2.imwrite("image.pgm", self.currentFrame)
			#cv2.imshow("Frame", self.currentFrame)
			
			#self.stream.truncate(0) #Must use this to eliminate the error: "Incorrect buffer length"
			
			key = cv2.waitKey(20) & 0xFF
		print("face loop stopped")
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
			#self.lock.acquire()
			frame_copy = np.array(self.currentGray)
			faces_copy = list(self.faces)
			#self.lock.release()
			return frame_copy, faces_copy
			
