import os
import csv
import constants

with open(constants.TRAINING_NEGATIVES_CSV_FILE, 'w') as csvfile:
	csv_writer = csv.writer(csvfile, dialect='excel')
	label = -1
	for root, dirs, nnf in os.walk(constants.TRAINING_NEGATIVE_IMAGES_DIR):
		for dir in dirs:
			for dirroot, nnd, files in os.walk(os.path.join(root, dir)):
				for name in files:
					if name.endswith('pgm'):
						path = os.path.join(root, dir, name)
						csv_writer.writerow([path, label])
						print("{}, {}".format(path, label))
			label = label - 1