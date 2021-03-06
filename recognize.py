import cv2
import numpy as np
from configparser import ConfigParser
import time

import constants
import face
from face import FaceVideoStreamFrame
from indoorpersontrackerapi import IndoorPersonTrackerAPI

class Recognizer:
	def __init__(self):
		self.video_frame = FaceVideoStreamFrame()
		self.video_frame.start()
		print('loading training data...')
		self.model = cv2.face.createFisherFaceRecognizer()
		self.model.load(constants.MODEL_FILE)
		self.persons = ConfigParser()
		self.persons.read('persons.ini')
		print('training data loaded!')
		print('connecting to tracker web service')
		# connect to the indoor person tracker web service
		self.isConnected = False
		self.tracker = IndoorPersonTrackerAPI()
		success = self.tracker.register(constants.IDENTIFIER)
		if success:
			print('connection is up!')
			self.isConnected = True
		else:
			print('connection failed!')
			self.isConnected = False

	def recognize(self):
		# take the current frame of the video stream for recognition
		grayscale, faces = self.video_frame.getCurrentFrame()
		for f in faces:
			x, y, w, h = f
			cropped = cv2.resize(grayscale[y:y+h, x:x+w], (constants.FACE_WIDTH, constants.FACE_HEIGHT))
			label, confidence = self.model.predict(cropped)
			if label > 0 and confidence <= 800:
				print("Hello {}! Confidence: {}".format(self.persons[str(label)]["name"], confidence))
				if self.isConnected:
					self.tracker.updateIdentificationCustomPFD(constants.IDENTIFIER, self.persons[str(label)]["name"], 0.0) # TODO calculate small probFalseDetection as a function from confidence
				time.sleep(1.0) # not trigger too often