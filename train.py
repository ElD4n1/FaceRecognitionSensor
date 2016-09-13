import cv2
import csv
import os
import numpy as np
from configparser import ConfigParser

import constants

def read_csv():
    csv_reader = csv.reader(open(constants.TRAINING_IMAGES_CSV_FILE, 'r'), dialect='excel')
    negatives_csv_reader = csv.reader(open(constants.TRAINING_NEGATIVES_CSV_FILE, 'r'), dialect='excel')
    training_faces = []
    labels = []
    labels_to_train = []
    persons = ConfigParser()
    persons.read('persons.ini')
    model_outdated = False
    for label in persons.sections():
        if persons[label]['is_trained'] == 'false':
            model_outdated = True
    if model_outdated:
        for label in persons.sections():
            #if persons[label]['is_trained'] == 'false':
                labels_to_train.append(label)
                persons[label]['is_trained'] = 'true'
                print("marked person for training: {} with label {}".format(persons[label]['name'], label))
        with open('persons.ini', 'w') as personsfile:
            persons.write(personsfile)
        for row in csv_reader:
            if row[1] in labels_to_train:
                training_faces.append(cv2.imread(row[0], cv2.IMREAD_GRAYSCALE))
                labels.append(int(row[1]))
        #config = ConfigParser()
        #config.read('config.ini')
        #if config['training']['negatives_trained'] == 'false': # model doesn't support update()
        print("marking negatives for training")
        for row in negatives_csv_reader:
            training_faces.append(cv2.resize(cv2.imread(row[0], cv2.IMREAD_GRAYSCALE), (constants.FACE_WIDTH, constants.FACE_HEIGHT)))
            labels.append(int(row[1]))
        #config['training']['negatives_trained'] = 'true'
        #with open('config.ini', 'w') as configfile:
            #config.write(configfile)
    return np.array(training_faces), np.array(labels)

def train():
    training_faces, labels = read_csv()
    if(len(training_faces) > 0 and len(labels) == len(training_faces)):
        model = cv2.face.createFisherFaceRecognizer()
        print("training model...this can take a while")
        model.train(training_faces, labels)
        filename = "training/model_fisherfaces.xml"
        model.save(filename)
        print("model trained")
    else:
        print("model is already up to date!")
