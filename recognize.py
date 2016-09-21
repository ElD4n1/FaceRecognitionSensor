import cv2
import numpy as np
from configparser import ConfigParser

import constants
import face
from face import FaceVideoStreamFrame
#from indoorpersontrackerapi import IndoorPersonTrackerAPI
import threading

class Recognizer(threading.Thread):
	def __init__(self):
		threading.Thread(self).__init__()
		self.video_frame = FaceVideoStreamFrame()
		self.video_frame.start()
		print('loading training data...')
		self.model = cv2.face.createFisherFaceRecognizer()
		self.model.load(constants.MODEL_FILE)
		self.persons = ConfigParser()
		self.persons.read('persons.ini')
		print('training data loaded!')
		#print('connecting to tracker web service')
		# connect to the indoor person tracker web service
		#self.isConnected = False
		#self.tracker = IndoorPersonTrackerAPI()
		#success = self.tracker.register(constants.IDENTIFIER)
		#if success:
		#	print('connection is up!')
		#	self.isConnected = True
		#else:
		#	print('connection failed!')
		#	self.isConnected = False
		self.lock = threading.Lock()
		self.recognized = []
		
	def run(self):
		# take the current frame of the video stream for recognition
		image = self.video_frame.getCurrentFrame()
		# convert image to grayscale
		grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# get coordinates of all faces in image
		
		faces = face.detect_faces(grayscale)
		for f in faces:
			x, y, w, h = f
			cropped = cv2.resize(grayscale[y:y+h, x:x+w], (constants.FACE_WIDTH, constants.FACE_HEIGHT))
			label, confidence = self.model.predict(cropped)
			if label > 0 and confidence <= 800:
				print("Hello {}! Confidence: {}".format(self.persons[str(label)]["name"], confidence))
				#if self.isConnected:
					#self.tracker.updateIdentificationCustomPFD(constants.IDENTIFIER, self.persons[str(label)]["name"], 0.0) # TODO calculate small probFalseDetection as a function from confidence
				self.recognized.append(self.persons[str(label)]["name"])
					
	def getRecognized(self):
		return self.recognized
