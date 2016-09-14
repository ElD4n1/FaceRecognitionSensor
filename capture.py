import glob
import os
import time
import threading
from configparser import ConfigParser

import cv2
import csv

import constants
import face
from face import FaceVideoStreamFrame

def capture(name):
	persons = ConfigParser()
	persons.read('persons.ini')
	label = -1
	if len(persons.sections()) > 0: # if there are alrdy persons registered
		for lbl in persons.sections():
			if persons[lbl]['name'] == name: # if this name is already registered (names must be unique)
				label = lbl
		if label == -1:
			label = int(persons.sections()[-1]) + 1 # get the last label and increment it for the next avail. label	
	else:
		label = 1
	file_prefix = "{}_{}_".format(label, name)
	# Create the directory for positive training images if it doesn't exist.
	if not os.path.exists(constants.TRAINING_POSITIVE_IMAGES_DIR):
		os.makedirs(constants.TRAINING_POSITIVE_IMAGES_DIR)
	csv_writer = csv.writer(open(constants.TRAINING_IMAGES_CSV_FILE, 'a'), dialect='excel')
	# Find the largest ID of existing positive images.
	# Start new images after this ID value.
	files = sorted(glob.glob(os.path.join(constants.TRAINING_POSITIVE_IMAGES_DIR, 
		file_prefix + '[0-9][0-9][0-9].pgm')))
	count = 0
	if len(files) > 0:
		# Grab the count from the last filename.
		count = int(files[-1][-7:-4])+1
	if count == 10: # if there are already 10 images for this person
		print('person {} already captured'.format(name))
		return
	video_frame = FaceVideoStreamFrame()
	video_frame.start()
	print('capturing positive training images.')
	print('press Ctrl-C to quit.')
	while count < 10:
		# Check if button was pressed or 'c' was received, then capture image.
		input("press enter to capture your face, remaining captures: {}".format(10 - count))
		print('capturing image...')
		image = video_frame.getCurrentFrame()
		# Convert image to grayscale.
		image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
		# Get coordinates of single face in captured image.
		faces = face.detect_faces(image)
		if len(faces) == 1:
			print("detected single face, processing it for training")
			x, y, w, h = faces[0]
			# Crop image as close as possible to desired face aspect ratio.
			# Might be smaller if face is near edge of image.
			cropped_image = cv2.resize(image[y:y+h, x:x+w], (constants.FACE_WIDTH, constants.FACE_HEIGHT))
			cv2.imshow("Recognized face", cropped_image)
			# Save image to file.
			filename = os.path.join(constants.TRAINING_POSITIVE_IMAGES_DIR, file_prefix + '%03d.pgm' % count)
			cv2.imwrite(filename, cropped_image)
			csv_writer.writerow([filename, label])
			print('found face and wrote training image {}'.format(filename))
			count += 1
		else:
			print("could not detect single face, faces detected: {}".format(len(faces)))
	strlabel = "{}".format(label)
	persons[strlabel] = {}
	persons[strlabel]['name'] = name
	persons[strlabel]['is_trained'] = 'false'
	with open('persons.ini', 'w') as personsfile:
		persons.write(personsfile)
	print("your face has been captured successfully!")
	video_frame.stop()