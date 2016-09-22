import cmd, sys
import cv2

import constants
import capture
import train
import time
from recognize import Recognizer
from face import FaceVideoStreamFrame
from face import FaceRectangles

class SensorShell(cmd.Cmd):
	intro = 'Hello, this is the sensor shell. Type ? or help to get a list of commands.\n'
	prompt = '$ '
	file = None
	
	def do_capture(self, arg):
		'Syntax: capture Name\nCapture a person with the specified name. (must be unique!)'
		if arg != '':
			capture.capture(arg)
		else:
			print("Syntax: capture Name")

	def do_train(self, arg):
		'Syntax: train\nTrain the model with all captured persons'
		train.train()

	def do_recognize(self, arg):
		'Syntax: recognize\nStart the recognize loop and try periodically to recongize all persons in the image'
		print("starting recognize loop, press 'C' to cancel")
		face_video_stream_frame = FaceVideoStreamFrame()
		face_video_stream_frame.start()
		recognizer = Recognizer()
		recognizer.start()
		key = 0
		time.sleep(2.0)
		while key != 'c' and key != 'C':
			recognizer.setData(face_video_stream_frame.getCurrentFrame(), face_video_stream_frame.getCurrentFaces())
			recognizer.getRecognized()
			key = cv2.waitKey(1)
	
	def do_exit(self, arg):
		'Exits the shell'
		sys.exit()

if __name__ == '__main__':
    SensorShell().cmdloop()
