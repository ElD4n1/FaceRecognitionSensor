import cv2
import threading
#from imutils.video import VideoStream
import picamera
import picamera.array
import imutils
import time

def detect_faces(image):
	haar_cascade = cv2.CascadeClassifier()
	haar_cascade.load('haarcascade_frontalface_default.xml')
	faces = haar_cascade.detectMultiScale(image)
	return faces

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (3240, 2464)
		
class FaceVideoStreamFrame(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		#self.vs = VideoStream(usePiCamera=True, resolution=(3240, 2464))
		self.isRunning = False
		self.currentFrame = stream.array
		
	def run(self):
		# initialize the video stream and allow the cammera sensor to warmup
		#self.vs.start()
		time.sleep(2.0)
		self.isRunning = True
		# loop over the frames from the video stream
		while self.isRunning:
			# grab the frame from the threaded video stream and resize it
			# to have a maximum width of 400 pixels
			#frame = self.vs.read()
			#frame = imutils.resize(frame, width=400)
			
			camera.capture(stream, 'bgr', use_video_port=True)
			frame = stream.array
			self.currentFrame = frame
			
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			faces = detect_faces(gray)

			# Draw a rectangle around the faces
			for (x, y, w, h) in faces:
				cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)

			# show the frame
			cv2.imshow("Frame", frame)
			
			stream.truncate(0) #Must use this to eliminate the error: "Incorrect buffer length"
			
			key = cv2.waitKey(10) & 0xFF
		cv2.destroyAllWindows()

	def stop(self):
		self.isRunning = False
		#self.vs.stop()
		print("VideoStream stopped, all resources freed")

	def getCurrentFrame(self):
		if(not self.isRunning):
			time.sleep(2.1)
		if(self.isRunning):
			#return self.vs.read()
			return self.currentFrame